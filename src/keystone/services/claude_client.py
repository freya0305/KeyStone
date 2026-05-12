"""Claude API client with cost tracking and circuit breaker.

Red team findings addressed:
- F1: Circuit breaker prevents cascading failures
- F2: Haiku 4K token cap prevents overflow truncation
- F3: Cost tracking per user per month
"""
import time
from dataclasses import dataclass
from typing import Generator

import anthropic
import structlog

from keystone.core import get_settings
from keystone.services.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    with_circuit_breaker,
    CircuitState,
)

logger = structlog.get_logger()

ANTHROPIC_PRICING = {
    "claude-haiku-4-20250514": {
        "input_tokens": 0.80 / 1_000_000,  # $0.80 per million
        "output_tokens": 4.00 / 1_000_000,  # $4.00 per million
    },
    "claude-sonnet-4-20250514": {
        "input_tokens": 3.00 / 1_000_000,  # $3.00 per million
        "output_tokens": 15.00 / 1_000_000,  # $15.00 per million
    },
}


@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    cost_sgd: float


@dataclass
class ClaudeResponse:
    content: str
    usage: TokenUsage
    model: str


class ClaudeClient:
    def __init__(self):
        self.settings = get_settings()
        self.client = anthropic.AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        self.circuit_breaker = CircuitBreaker(
            config=anthropic.APIError,
        )

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in SGD."""
        pricing = ANTHROPIC_PRICING.get(model, ANTHROPIC_PRICING["claude-haiku-4-20250514"])
        cost = (input_tokens * pricing["input_tokens"] + output_tokens * pricing["output_tokens"])
        # Convert USD to SGD (approximate)
        return cost * 1.34

    async def generate(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        timeout: float = 30.0,
    ) -> ClaudeResponse:
        """Generate content with Claude API with circuit breaker protection.

        Args:
            model: Model to use (haiku or sonnet)
            system_prompt: System prompt
            user_prompt: User prompt
            max_tokens: Max output tokens (capped at 4096 for Haiku)
            timeout: Request timeout in seconds (default 30s; resume analysis ≤10s, suggestions ≤15s per spec)

        Returns:
            ClaudeResponse with content and token usage
        """
        # Red team F2: Enforce 4K cap on Haiku to prevent overflow truncation
        if model == self.settings.anthropic_model_haiku:
            max_tokens = min(max_tokens, self.settings.anthropic_max_tokens_haiku)

        def call_api() -> anthropic.messages.message.Message:
            return self.client.messages.sync.create(
                model=model,
                system=system_prompt,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": user_prompt}],
                timeout=timeout,
            )

        try:
            # Use circuit breaker for API protection
            if self.circuit_breaker.can_attempt():
                response = await with_circuit_breaker(
                    self.circuit_breaker,
                    call_api,
                )
            else:
                raise CircuitBreakerError("Claude API circuit breaker is open")

        except CircuitBreakerError:
            raise
        except Exception as e:
            self.circuit_breaker.record_failure()
            logger.error("claude_api_error", error=str(e), model=model)
            raise

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost_sgd = self._calculate_cost(model, input_tokens, output_tokens)

        # Log token usage for cost monitoring
        logger.info(
            "claude_api_call",
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_sgd=cost_sgd,
        )

        return ClaudeResponse(
            content=response.content[0].text,
            usage=TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_sgd=cost_sgd,
            ),
            model=model,
        )

    async def generate_stream(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> Generator[str, None, None]:
        """Stream generation with Claude API."""
        if model == self.settings.anthropic_model_haiku:
            max_tokens = min(max_tokens, self.settings.anthropic_max_tokens_haiku)

        def call_api_stream():
            return self.client.messages.stream(
                model=model,
                system=system_prompt,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": user_prompt}],
            )

        try:
            if not self.circuit_breaker.can_attempt():
                raise CircuitBreakerError("Claude API circuit breaker is open")

            with self.circuit_breaker:
                with self.client.messages.stream(
                    model=model,
                    system=system_prompt,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": user_prompt}],
                ) as stream:
                    for text_event in stream.text_stream:
                        yield text_event
        except CircuitBreakerError:
            raise
        except Exception as e:
            self.circuit_breaker.record_failure()
            logger.error("claude_api_stream_error", error=str(e), model=model)
            raise


# Global instance
_claude_client: ClaudeClient | None = None


def get_claude_client() -> ClaudeClient:
    """Get or create Claude client singleton."""
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client
