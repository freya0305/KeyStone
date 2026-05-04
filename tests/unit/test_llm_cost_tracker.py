"""Tests for LLM cost tracker - SGD 5/month ceiling."""
import pytest
from unittest.mock import MagicMock, patch


class TestLLMCostTracker:
    """LLM cost tracker tests."""

    def test_cost_calculation_haiku(self):
        """Haiku cost should be calculated correctly."""
        from keystone.services.llm_cost_tracker import _calculate_cost

        # Haiku input: $0.80/1M, output: $4.00/1M (SGD rates)
        # 1000 tokens input, 500 tokens output
        cost = _calculate_cost("claude-haiku-4-20250514", 1000, 500)
        # (1000 * 0.80/1M + 500 * 4.00/1M) * 1.34 (USD->SGD conversion)
        expected = ((1000 * 0.80 / 1_000_000) + (500 * 4.00 / 1_000_000)) * 1.34
        assert abs(cost - expected) < 0.0001

    def test_cost_calculation_sonnet(self):
        """Sonnet cost should be calculated correctly."""
        from keystone.services.llm_cost_tracker import _calculate_cost

        # Sonnet input: $3/1M, output: $15/1M (SGD rates)
        cost = _calculate_cost("claude-sonnet-4-20250514", 1000, 500)
        expected = ((1000 * 3.00 / 1_000_000) + (500 * 15.00 / 1_000_000)) * 1.34
        assert abs(cost - expected) < 0.0001

    def test_cost_calculation_unknown_model(self):
        """Unknown model should use default rates."""
        from keystone.services.llm_cost_tracker import _calculate_cost

        # Unknown uses DEFAULT_COST_RATES (Sonnet rates)
        cost = _calculate_cost("unknown-model", 1000, 500)
        expected = ((1000 * 3.00 / 1_000_000) + (500 * 15.00 / 1_000_000)) * 1.34
        assert abs(cost - expected) < 0.0001


class TestCostTrackerIntegration:
    """Integration tests for cost tracker with Redis."""

    def test_month_key_format(self):
        """Month key should be YYYY-MM format."""
        from keystone.services.llm_cost_tracker import _get_month_key

        key = _get_month_key()
        assert len(key) == 7
        assert key[4] == "-"

    def test_cost_key_format(self):
        """Cost key should include user_id and month."""
        from keystone.services.llm_cost_tracker import _get_cost_key

        key = _get_cost_key("user-123")
        assert "user-123" in key
        assert "llm_cost" in key
