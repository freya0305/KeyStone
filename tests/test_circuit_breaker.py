"""Tests for circuit breaker."""
import pytest
import asyncio

from keystone.services.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    with_circuit_breaker,
    CircuitState,
)


class TestCircuitBreaker:
    """Test circuit breaker functionality."""

    def test_initial_state_is_closed(self):
        breaker = CircuitBreaker()
        assert breaker.state == CircuitState.CLOSED
        assert breaker.can_attempt() is True

    def test_opens_after_failure_threshold(self):
        breaker = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=3))

        for _ in range(3):
            breaker.record_failure()

        assert breaker.state == CircuitState.OPEN
        assert breaker.can_attempt() is False

    def test_resets_on_success(self):
        breaker = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=2))

        breaker.record_failure()
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        breaker.record_success()
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0

    @pytest.mark.asyncio
    async def test_circuit_breaker_error_when_open(self):
        breaker = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=1, recovery_timeout=60))

        # Open the circuit
        breaker.record_failure()

        async def failing_func():
            return "should not be called"

        with pytest.raises(CircuitBreakerError) as exc_info:
            await with_circuit_breaker(breaker, failing_func)

        assert "open" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_success_returns_value(self):
        breaker = CircuitBreaker()

        async def success_func():
            return "success"

        result = await with_circuit_breaker(breaker, success_func)
        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
