"""Tests for circuit breaker."""
import pytest

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

    def test_half_open_after_recovery_timeout(self):
        """Test that circuit transitions to HALF_OPEN after recovery timeout."""
        import time
        breaker = CircuitBreaker(
            config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=1.0)
        )

        # Open the circuit
        for _ in range(3):
            breaker.record_failure()
        assert breaker.state == CircuitState.OPEN
        assert breaker.can_attempt() is False

        # Wait for recovery timeout
        time.sleep(1.1)

        # Should transition to HALF_OPEN
        assert breaker.can_attempt() is True
        assert breaker.state == CircuitState.HALF_OPEN

    def test_failure_in_half_open_reopens_circuit(self):
        """Test that failure in HALF_OPEN state reopens the circuit."""
        import time
        breaker = CircuitBreaker(
            config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=0.1)
        )

        # Open the circuit
        for _ in range(3):
            breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)

        # Transition to HALF_OPEN
        assert breaker.can_attempt() is True
        assert breaker.state == CircuitState.HALF_OPEN

        # Record a failure in HALF_OPEN
        breaker.record_failure()

        # Should reopen the circuit
        assert breaker.state == CircuitState.OPEN

    def test_success_in_half_open_closes_circuit(self):
        """Test that success in HALF_OPEN state closes the circuit."""
        import time
        breaker = CircuitBreaker(
            config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=0.1)
        )

        # Open the circuit
        for _ in range(3):
            breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)

        # Transition to HALF_OPEN
        assert breaker.can_attempt() is True
        assert breaker.state == CircuitState.HALF_OPEN

        # Record success in HALF_OPEN
        breaker.record_success()

        # Should close the circuit
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0
