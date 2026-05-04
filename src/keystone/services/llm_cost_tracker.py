"""LLM Cost Tracker - Tracks Claude API costs per user per month.

Implements SGD 5/user/month ceiling with Redis backend and in-memory fallback.
Admin alerts at 80% and 100% thresholds.
"""
import threading
import time
from collections import defaultdict
from datetime import datetime
from typing import Optional

import structlog

from keystone.core import get_settings

logger = structlog.get_logger()

# Cost rates per model (SGD per million tokens)
LLM_COST_RATES = {
    "claude-haiku-4-20250514": {
        "input_tokens": 0.80 / 1_000_000,  # $0.80 per million
        "output_tokens": 4.00 / 1_000_000,  # $4.00 per million
    },
    "claude-sonnet-4-20250514": {
        "input_tokens": 3.00 / 1_000_000,  # $3.00 per million
        "output_tokens": 15.00 / 1_000_000,  # $15.00 per million
    },
}

# Fallback rates for unknown models (use Sonnet rates)
DEFAULT_COST_RATES = {
    "input_tokens": 3.00 / 1_000_000,
    "output_tokens": 15.00 / 1_000_000,
}

# In-memory fallback store
_memory_store: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
_memory_lock = threading.Lock()
_last_cleanup = time.time()
_MEMORY_CLEANUP_INTERVAL = 3600  # 1 hour


def _get_month_key() -> str:
    """Get the current month key in YYYY-MM format."""
    return datetime.utcnow().strftime("%Y-%m")


def _get_cost_key(user_id: str) -> str:
    """Get the Redis key for a user's monthly cost."""
    month_key = _get_month_key()
    return f"llm_cost:{user_id}:{month_key}"


def _get_warning_key(user_id: str) -> str:
    """Get the Redis key for tracking if warning was sent."""
    month_key = _get_month_key()
    return f"llm_cost_warning:{user_id}:{month_key}"


def _cleanup_memory_store() -> None:
    """Remove expired entries from memory store."""
    global _last_cleanup
    now = time.time()

    if now - _last_cleanup < _MEMORY_CLEANUP_INTERVAL:
        return

    _last_cleanup = now
    current_month = _get_month_key()

    with _memory_lock:
        expired_keys = [
            k for k in _memory_store.keys() if not k.endswith(current_month)
        ]
        for k in expired_keys:
            del _memory_store[k]


def _calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in SGD for a given model and token usage."""
    rates = LLM_COST_RATES.get(model, DEFAULT_COST_RATES)
    cost = (input_tokens * rates["input_tokens"] + output_tokens * rates["output_tokens"])
    # Convert USD to SGD (approximate)
    return cost * 1.34


class LLMCostTracker:
    """Tracks LLM costs per user with Redis backend and in-memory fallback.

    Uses Redis when available, falls back to in-memory store.
    Cost ceiling is SGD 5/user/month by default (configurable).
    """

    def __init__(self):
        self.settings = get_settings()
        self._redis_client = None
        self._redis_available = None
        self._check_redis()

    def _check_redis(self) -> None:
        """Check if Redis is available and initialize client."""
        if self._redis_available is not None:
            return

        try:
            import redis
            self._redis_client = redis.from_url(
                self.settings.redis_url,
                decode_responses=True,
            )
            # Test connection
            self._redis_client.ping()
            self._redis_available = True
            logger.info("llm_cost_tracker_redis_available")
        except Exception as e:
            self._redis_available = False
            self._redis_client = None
            logger.warning(
                "llm_cost_tracker_redis_unavailable",
                error=str(e),
                using="in_memory_fallback",
            )

    @property
    def is_redis_available(self) -> bool:
        """Check if Redis is available."""
        if self._redis_available is None:
            self._check_redis()
        return self._redis_available

    def get_user_cost(self, user_id: str) -> float:
        """Get the current month's cost for a user.

        Args:
            user_id: The user's ID

        Returns:
            Total cost in SGD for the current month
        """
        if self.is_redis_available and self._redis_client:
            try:
                key = _get_cost_key(user_id)
                cost = self._redis_client.get(key)
                return float(cost) if cost else 0.0
            except Exception as e:
                logger.warning("llm_cost_get_redis_failed", error=str(e), user_id=user_id)

        # Fallback to memory store
        _cleanup_memory_store()
        with _memory_lock:
            month_key = _get_month_key()
            return _memory_store[user_id].get(month_key, 0.0)

    def add_cost(
        self,
        user_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Add cost for a user's LLM call.

        Args:
            user_id: The user's ID
            model: The model used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            The cost added in SGD
        """
        cost = _calculate_cost(model, input_tokens, output_tokens)
        settings = get_settings()
        ceiling = settings.llm_cost_ceiling_sgd
        warning_threshold = settings.llm_cost_warning_threshold

        if self.is_redis_available and self._redis_client:
            try:
                key = _get_cost_key(user_id)
                warning_key = _get_warning_key(user_id)

                # Increment cost in Redis
                pipe = self._redis_client.pipeline()
                pipe.incrbyfloat(key, cost)
                pipe.expire(key, 60 * 60 * 24 * 35)  # 35 day TTL
                pipe.execute()

                # Get new total
                new_cost = float(self._redis_client.get(key))

                # Check thresholds and alert
                self._check_and_alert(user_id, new_cost, ceiling, warning_threshold, warning_key)

                return cost
            except Exception as e:
                logger.warning("llm_cost_add_redis_failed", error=str(e), user_id=user_id)

        # Fallback to memory store
        _cleanup_memory_store()
        with _memory_lock:
            month_key = _get_month_key()
            new_cost = _memory_store[user_id][month_key] + cost

            if new_cost > ceiling * 1.5:
                # Cap at 150% to prevent runaway
                new_cost = ceiling * 1.5

            _memory_store[user_id][month_key] = new_cost

            # Check thresholds
            self._check_and_alert_memory(user_id, new_cost, ceiling, warning_threshold)

        logger.info(
            "llm_cost_added",
            user_id=user_id,
            cost_sgd=cost,
            total_monthly=new_cost,
            model=model,
        )

        return cost

    def _check_and_alert(
        self,
        user_id: str,
        new_cost: float,
        ceiling: float,
        warning_threshold: float,
        warning_key: str,
    ) -> None:
        """Check cost thresholds and send alerts via Redis."""
        try:
            # Check if already alerted this month
            alerted = self._redis_client.get(warning_key)
            if alerted:
                return

            percentage = (new_cost / ceiling) * 100

            if percentage >= 100:
                logger.error(
                    "llm_cost_ceiling_reached",
                    user_id=user_id,
                    cost_sgd=new_cost,
                    ceiling_sgd=ceiling,
                    percentage=percentage,
                )
                # Alert admin - in production this would trigger a notification
                self._send_admin_alert(user_id, new_cost, ceiling, "100%")
                # Mark as alerted
                self._redis_client.setex(warning_key, 60 * 60 * 24 * 35, "100")

            elif percentage >= warning_threshold * 100:
                logger.warning(
                    "llm_cost_warning_threshold",
                    user_id=user_id,
                    cost_sgd=new_cost,
                    ceiling_sgd=ceiling,
                    percentage=percentage,
                )
                self._send_admin_alert(user_id, new_cost, ceiling, f"{percentage:.0f}%")
                # Mark as alerted at this threshold
                self._redis_client.setex(warning_key, 60 * 60 * 24 * 35, f"{percentage:.0f}")

        except Exception as e:
            logger.warning("llm_cost_alert_check_failed", error=str(e))

    def _check_and_alert_memory(
        self,
        user_id: str,
        new_cost: float,
        ceiling: float,
        warning_threshold: float,
    ) -> None:
        """Check cost thresholds for memory backend."""
        percentage = (new_cost / ceiling) * 100

        if percentage >= 100:
            logger.error(
                "llm_cost_ceiling_reached",
                user_id=user_id,
                cost_sgd=new_cost,
                ceiling_sgd=ceiling,
                percentage=percentage,
                backend="memory",
            )
            self._send_admin_alert(user_id, new_cost, ceiling, "100%")

        elif percentage >= warning_threshold * 100:
            logger.warning(
                "llm_cost_warning_threshold",
                user_id=user_id,
                cost_sgd=new_cost,
                ceiling_sgd=ceiling,
                percentage=percentage,
                backend="memory",
            )
            self._send_admin_alert(user_id, new_cost, ceiling, f"{percentage:.0f}%")

    def _send_admin_alert(
        self,
        user_id: str,
        cost: float,
        ceiling: float,
        percentage: str,
    ) -> None:
        """Send admin alert for cost threshold breach.

        In production, this would integrate with alerting system (Sentry, PagerDuty, etc.)
        """
        logger.warning(
            "llm_cost_admin_alert",
            alert_type="cost_threshold",
            user_id=user_id,
            cost_sgd=cost,
            ceiling_sgd=ceiling,
            percentage=percentage,
        )

    def is_ceiling_reached(self, user_id: str) -> bool:
        """Check if a user has reached their cost ceiling.

        Args:
            user_id: The user's ID

        Returns:
            True if ceiling is reached, False otherwise
        """
        settings = get_settings()
        current_cost = self.get_user_cost(user_id)
        return current_cost >= settings.llm_cost_ceiling_sgd

    def get_remaining_budget(self, user_id: str) -> float:
        """Get remaining budget for a user.

        Args:
            user_id: The user's ID

        Returns:
            Remaining budget in SGD (can be negative if over ceiling)
        """
        settings = get_settings()
        current_cost = self.get_user_cost(user_id)
        return max(0.0, settings.llm_cost_ceiling_sgd - current_cost)

    def get_cost_status(self, user_id: str) -> dict:
        """Get detailed cost status for a user.

        Returns:
            Dict with cost, ceiling, remaining, and percentage
        """
        settings = get_settings()
        current_cost = self.get_user_cost(user_id)
        ceiling = settings.llm_cost_ceiling_sgd
        remaining = max(0.0, ceiling - current_cost)
        percentage = (current_cost / ceiling) * 100 if ceiling > 0 else 0

        return {
            "current_cost_sgd": current_cost,
            "ceiling_sgd": ceiling,
            "remaining_sgd": remaining,
            "percentage_used": percentage,
            "ceiling_reached": current_cost >= ceiling,
            "backend": "redis" if self.is_redis_available else "memory",
        }


# Global instance
_llm_cost_tracker: Optional[LLMCostTracker] = None


def get_llm_cost_tracker() -> LLMCostTracker:
    """Get or create the LLM cost tracker singleton."""
    global _llm_cost_tracker
    if _llm_cost_tracker is None:
        _llm_cost_tracker = LLMCostTracker()
    return _llm_cost_tracker
