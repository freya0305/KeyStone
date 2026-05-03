"""Circuit breaker for external API calls.

Prevents cascading failures when Claude API is down.
Red team finding: Claude API failure = entire product fails.
"""
import asyncio
import time
from enum import Enum
from typing import Callable, TypeVar, Any
from dataclasses import dataclass, field

import structlog

logger = structlog.get_logger()


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject calls immediately
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5  # Open after 5 consecutive failures
    recovery_timeout: float = 60.0  # Try again after 60 seconds
    expected_exception: type = Exception


@dataclass
class CircuitBreaker:
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: float = field(default_factory=time.time)
    config: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning("circuit_breaker_opened", failure_count=self.failure_count)

    def can_attempt(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.config.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                logger.info("circuit_breaker_half_open", time_since_failure=time.time() - self.last_failure_time)
                return True
            return False
        return False


T = TypeVar("T")


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""
    pass


async def with_circuit_breaker(
    breaker: CircuitBreaker,
    func: Callable[..., T],
    *args: Any,
    **kwargs: Any,
) -> T:
    """Execute a function with circuit breaker protection.

    Args:
        breaker: CircuitBreaker instance
        func: Async function to call
        *args, **kwargs: Arguments to pass to func

    Returns:
        Result of func()

    Raises:
        CircuitBreakerError: If circuit is open
    """
    if not breaker.can_attempt():
        raise CircuitBreakerError(
            f"Circuit breaker is {breaker.state.value}. "
            f"Try again in {breaker.config.recovery_timeout - (time.time() - breaker.last_failure_time):.0f}s."
        )

    try:
        result = await func(*args, **kwargs)
        breaker.record_success()
        return result
    except breaker.config.expected_exception as e:
        breaker.record_failure()
        logger.error("circuit_breaker_call_failed", error=str(e), state=breaker.state.value)
        raise
