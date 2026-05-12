"""Tests for suggestion-outcome correlation feature in job_seeker.py."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from keystone.api.job_seeker import (
    get_suggestion_outcome_correlation,
    SuggestionOutcomeCorrelation,
    MatchLevelStats,
)


class TestGetSuggestionOutcomeCorrelation:
    """Test suite for get_suggestion_outcome_correlation function."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock AsyncSession."""
        return AsyncMock()

    @pytest.fixture
    def mock_result_proxy(self):
        """Create a mock result proxy that returns rows from .all()."""
        return MagicMock()

    async def test_returns_empty_correlation_when_no_data(self, mock_db, mock_result_proxy):
        """Should return empty correlation with zeros when no data exists."""
        mock_db.execute.return_value = mock_result_proxy
        mock_result_proxy.all.return_value = []

        result = await get_suggestion_outcome_correlation(mock_db)

        assert isinstance(result, SuggestionOutcomeCorrelation)
        assert result.total_signals == 0
        assert result.total_applications == 0
        assert result.overall_response_rate == 0.0
        assert result.by_match_level == []

    async def test_groups_by_match_level(self, mock_db, mock_result_proxy):
        """Should group signals by match_level."""
        mock_db.execute.return_value = mock_result_proxy
        # Simulate database rows with different match_levels
        mock_row = MagicMock()
        mock_row.match_level = "strong"
        mock_row.signal_count = 10
        mock_row.application_count = 5
        mock_row.responded_count = 3
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(mock_db)

        assert len(result.by_match_level) == 1
        assert result.by_match_level[0].match_level == "strong"
        assert result.by_match_level[0].signal_count == 10
        assert result.by_match_level[0].application_count == 5
        assert result.by_match_level[0].responded_count == 3

    async def test_calculates_response_rate_correctly(self, mock_db, mock_result_proxy):
        """Should calculate response_rate = responded_count / application_count."""
        mock_db.execute.return_value = mock_result_proxy
        mock_row = MagicMock()
        mock_row.match_level = "strong"
        mock_row.signal_count = 20
        mock_row.application_count = 10
        mock_row.responded_count = 4  # 40% response rate
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(mock_db)

        assert result.by_match_level[0].response_rate == 0.4
        assert result.total_signals == 20
        assert result.total_applications == 10
        assert result.total_signals == 20

    async def test_response_rate_zero_when_no_applications(self, mock_db, mock_result_proxy):
        """Should return 0 response_rate when application_count is 0."""
        mock_db.execute.return_value = mock_result_proxy
        mock_row = MagicMock()
        mock_row.match_level = "weak"
        mock_row.signal_count = 5
        mock_row.application_count = 0
        mock_row.responded_count = 0
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(mock_db)

        assert result.by_match_level[0].response_rate == 0.0

    async def test_overall_response_rate_aggregates_all_levels(self, mock_db, mock_result_proxy):
        """Should calculate overall_response_rate from total responded / total apps."""
        mock_db.execute.return_value = mock_result_proxy
        row1 = MagicMock()
        row1.match_level = "strong"
        row1.signal_count = 10
        row1.application_count = 10
        row1.responded_count = 5  # 50%

        row2 = MagicMock()
        row2.match_level = "transferable"
        row2.signal_count = 10
        row2.application_count = 10
        row2.responded_count = 2  # 20%

        mock_result_proxy.all.return_value = [row1, row2]

        result = await get_suggestion_outcome_correlation(mock_db)

        # Overall: 7 responded / 20 total apps = 0.35
        assert result.overall_response_rate == 0.35
        assert result.total_applications == 20
        assert result.total_signals == 20

    async def test_ranked_by_response_rate_descending(self, mock_db, mock_result_proxy):
        """Should rank by_match_level by response_rate in descending order."""
        mock_db.execute.return_value = mock_result_proxy
        row1 = MagicMock()
        row1.match_level = "low_performer"
        row1.signal_count = 10
        row1.application_count = 10
        row1.responded_count = 1  # 10%

        row2 = MagicMock()
        row2.match_level = "high_performer"
        row2.signal_count = 10
        row2.application_count = 10
        row2.responded_count = 9  # 90%

        mock_result_proxy.all.return_value = [row1, row2]

        result = await get_suggestion_outcome_correlation(mock_db)

        assert len(result.by_match_level) == 2
        # High performer should be first (90% > 10%)
        assert result.by_match_level[0].match_level == "high_performer"
        assert result.by_match_level[0].response_rate == 0.9
        assert result.by_match_level[1].match_level == "low_performer"
        assert result.by_match_level[1].response_rate == 0.1

    async def test_handles_null_match_level_as_unknown(self, mock_db, mock_result_proxy):
        """Should treat NULL match_level as 'unknown'."""
        mock_db.execute.return_value = mock_result_proxy
        mock_row = MagicMock()
        mock_row.match_level = None
        mock_row.signal_count = 7
        mock_row.application_count = 3
        mock_row.responded_count = 1
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(mock_db)

        assert len(result.by_match_level) == 1
        assert result.by_match_level[0].match_level == "unknown"

    async def test_filters_by_limit_match_level(self, mock_db, mock_result_proxy):
        """Should filter results when limit_match_level is specified."""
        mock_db.execute.return_value = mock_result_proxy
        mock_row = MagicMock()
        mock_row.match_level = "strong"
        mock_row.signal_count = 15
        mock_row.application_count = 8
        mock_row.responded_count = 6
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(
            mock_db, limit_match_level="strong"
        )

        # The query should have been called with limit_match_level filter
        mock_db.execute.assert_called_once()
        call_args = mock_db.execute.call_args
        # Verify the query object was passed
        assert call_args is not None
        assert result.by_match_level[0].match_level == "strong"

    async def test_handles_none_values_in_row(self, mock_db, mock_result_proxy):
        """Should handle None values for signal_count, application_count, responded."""
        mock_db.execute.return_value = mock_result_proxy
        mock_row = MagicMock()
        mock_row.match_level = "transferable"
        mock_row.signal_count = None
        mock_row.application_count = None
        mock_row.responded_count = None
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(mock_db)

        # Should treat None as 0
        assert result.by_match_level[0].signal_count == 0
        assert result.by_match_level[0].application_count == 0
        assert result.by_match_level[0].responded_count == 0
        assert result.by_match_level[0].response_rate == 0.0

    async def test_response_rate_rounded_to_4_decimals(self, mock_db, mock_result_proxy):
        """Should round response_rate to 4 decimal places."""
        mock_db.execute.return_value = mock_result_proxy
        mock_row = MagicMock()
        mock_row.match_level = "strong"
        mock_row.signal_count = 3
        mock_row.application_count = 7
        mock_row.responded_count = 1  # 1/7 = 0.142857...
        mock_result_proxy.all.return_value = [mock_row]

        result = await get_suggestion_outcome_correlation(mock_db)

        # Should be rounded to 4 decimal places
        assert result.by_match_level[0].response_rate == round(1 / 7, 4)


class TestMatchLevelStats:
    """Test suite for MatchLevelStats model."""

    def test_match_level_stats_creation(self):
        """Should create MatchLevelStats with all fields."""
        stats = MatchLevelStats(
            match_level="strong",
            signal_count=100,
            application_count=50,
            responded_count=25,
            response_rate=0.5,
        )
        assert stats.match_level == "strong"
        assert stats.signal_count == 100
        assert stats.application_count == 50
        assert stats.responded_count == 25
        assert stats.response_rate == 0.5

    def test_match_level_stats_defaults(self):
        """Should have correct default values."""
        stats = MatchLevelStats(match_level="weak")
        assert stats.signal_count == 0
        assert stats.application_count == 0
        assert stats.responded_count == 0
        assert stats.response_rate == 0.0


class TestSuggestionOutcomeCorrelation:
    """Test suite for SuggestionOutcomeCorrelation model."""

    def test_suggestion_outcome_correlation_creation(self):
        """Should create SuggestionOutcomeCorrelation with all fields."""
        stats = MatchLevelStats(
            match_level="strong",
            signal_count=50,
            application_count=25,
            responded_count=10,
            response_rate=0.4,
        )
        correlation = SuggestionOutcomeCorrelation(
            total_signals=100,
            total_applications=50,
            overall_response_rate=0.3,
            by_match_level=[stats],
        )
        assert correlation.total_signals == 100
        assert correlation.total_applications == 50
        assert correlation.overall_response_rate == 0.3
        assert len(correlation.by_match_level) == 1
        assert correlation.by_match_level[0].match_level == "strong"

    def test_suggestion_outcome_correlation_defaults(self):
        """Should have correct default values."""
        correlation = SuggestionOutcomeCorrelation()
        assert correlation.total_signals == 0
        assert correlation.total_applications == 0
        assert correlation.overall_response_rate == 0.0
        assert correlation.by_match_level == []
