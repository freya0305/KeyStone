"""Tests for gamification feature - streak tracking and badge awards."""
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from keystone.api.job_seeker import (
    BADGE_DEFINITIONS,
    BadgeDefinition,
    GamificationStats,
    _compute_gamification_stats,
    _update_gamification_on_activity,
)


class TestBadgeDefinitions:
    """Badge definition validation tests."""

    def test_badge_definitions_is_list(self):
        """BADGE_DEFINITIONS should be a list."""
        assert isinstance(BADGE_DEFINITIONS, list)
        assert len(BADGE_DEFINITIONS) > 0

    def test_all_badges_have_required_fields(self):
        """Every badge should have id, name, description, and icon."""
        required_fields = {"id", "name", "description", "icon"}
        for badge in BADGE_DEFINITIONS:
            assert required_fields.issubset(badge.keys()), f"Badge {badge} missing fields"
            assert isinstance(badge["id"], str)
            assert isinstance(badge["name"], str)
            assert isinstance(badge["description"], str)
            assert isinstance(badge["icon"], str)

    def test_all_badge_ids_are_unique(self):
        """Badge IDs should be unique."""
        badge_ids = [b["id"] for b in BADGE_DEFINITIONS]
        assert len(badge_ids) == len(set(badge_ids)), "Duplicate badge IDs found"

    def test_streak_badges_exist(self):
        """Streak badges should exist for 3, 7, and 14 day streaks."""
        streak_badge_ids = {"streak_3", "streak_7", "streak_14"}
        actual_ids = {b["id"] for b in BADGE_DEFINITIONS}
        assert streak_badge_ids.issubset(actual_ids), f"Missing streak badges: {streak_badge_ids - actual_ids}"

    def test_application_count_badges_exist(self):
        """Application count badges should exist for 5, 10, and 25 apps."""
        app_badge_ids = {"apps_5", "apps_10", "apps_25"}
        actual_ids = {b["id"] for b in BADGE_DEFINITIONS}
        assert app_badge_ids.issubset(actual_ids), f"Missing app badges: {app_badge_ids - actual_ids}"

    def test_first_activity_badges_exist(self):
        """First activity badges should exist."""
        first_badge_ids = {"first_app", "first_outcome"}
        actual_ids = {b["id"] for b in BADGE_DEFINITIONS}
        assert first_badge_ids.issubset(actual_ids), f"Missing first badges: {first_badge_ids - actual_ids}"

    def test_response_and_interview_badges_exist(self):
        """Response and interview badges should exist."""
        milestone_badge_ids = {"response_received", "interview_1"}
        actual_ids = {b["id"] for b in BADGE_DEFINITIONS}
        assert milestone_badge_ids.issubset(actual_ids), f"Missing milestone badges: {milestone_badge_ids - actual_ids}"


class TestComputeGamificationStats:
    """_compute_gamification_stats function tests."""

    def test_returns_gamification_stats(self):
        """Should return a GamificationStats object."""
        result = _compute_gamification_stats(
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            earned_badges={},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        assert isinstance(result, GamificationStats)

    def test_current_and_longest_streak_returned(self):
        """Should return current and longest streak values."""
        result = _compute_gamification_stats(
            current_streak=5,
            longest_streak=10,
            last_activity_date=None,
            earned_badges={},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        assert result.current_streak == 5
        assert result.longest_streak == 10

    def test_last_activity_date_none_when_no_activity(self):
        """Should return None last_activity_date when no activity."""
        result = _compute_gamification_stats(
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            earned_badges={},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        assert result.last_activity_date is None

    def test_last_activity_date_iso_format(self):
        """Should return ISO format date string when activity exists."""
        activity_date = date(2024, 3, 15)
        result = _compute_gamification_stats(
            current_streak=1,
            longest_streak=1,
            last_activity_date=activity_date,
            earned_badges={},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        assert result.last_activity_date == "2024-03-15"

    def test_all_badges_returned(self):
        """Should return all badges from BADGE_DEFINITIONS."""
        result = _compute_gamification_stats(
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            earned_badges={},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        assert len(result.badges) == len(BADGE_DEFINITIONS)

    def test_badge_earned_false_when_not_in_earned_badges(self):
        """Badge should have earned=False when not in earned_badges."""
        result = _compute_gamification_stats(
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            earned_badges={},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        for badge in result.badges:
            assert badge.earned is False
            assert badge.earned_at is None

    def test_badge_earned_true_when_in_earned_badges(self):
        """Badge should have earned=True and earned_at when in earned_badges."""
        earned_time = "2024-03-15T10:30:00"
        result = _compute_gamification_stats(
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            earned_badges={"first_app": earned_time},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        first_app_badge = next(b for b in result.badges if b.id == "first_app")
        assert first_app_badge.earned is True
        assert first_app_badge.earned_at == earned_time

    def test_non_earned_badge_keeps_earned_false(self):
        """Non-earned badges should still have earned=False even when other badges are earned."""
        earned_time = "2024-03-15T10:30:00"
        result = _compute_gamification_stats(
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
            earned_badges={"first_app": earned_time},
            total_applications=0,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        streak_badge = next(b for b in result.badges if b.id == "streak_3")
        assert streak_badge.earned is False

    def test_earned_badges_dict_format(self):
        """Should handle earned_badges as dict with badge_id -> iso_time mapping."""
        earned_time = "2024-03-15T10:30:00"
        result = _compute_gamification_stats(
            current_streak=5,
            longest_streak=5,
            last_activity_date=date.today(),
            earned_badges={"streak_3": earned_time, "apps_5": earned_time},
            total_applications=5,
            has_outcome=False,
            has_response=False,
            has_interview=False,
        )
        streak_badge = next(b for b in result.badges if b.id == "streak_3")
        apps_badge = next(b for b in result.badges if b.id == "apps_5")
        assert streak_badge.earned is True
        assert apps_badge.earned is True


class TestUpdateGamificationOnActivity:
    """_update_gamification_on_activity function tests."""

    @pytest.fixture
    def mock_user(self):
        """Create a mock user object."""
        user = MagicMock()
        user.id = uuid4()
        user.current_streak = 0
        user.longest_streak = 0
        user.last_activity_date = None
        user.earned_badges = {}
        return user

    def _make_user_result(self, mock_user):
        """Create a mock result for user query."""
        result = MagicMock()
        result.scalar_one_or_none.return_value = mock_user
        return result

    def _make_apps_result(self, apps):
        """Create a mock result for applications query."""
        result = MagicMock()
        result.scalars.return_value.all.return_value = apps
        return result

    @pytest.mark.asyncio
    async def test_first_activity_sets_streak_to_one(self, mock_user):
        """First activity ever should set current_streak to 1."""
        mock_user.last_activity_date = None

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert mock_user.current_streak == 1
        assert mock_user.longest_streak == 1

    @pytest.mark.asyncio
    async def test_same_day_does_not_change_streak(self, mock_user):
        """Same day activity should not change streak."""
        today = date.today()
        mock_user.last_activity_date = today
        mock_user.current_streak = 5
        mock_user.longest_streak = 5

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert mock_user.current_streak == 5

    @pytest.mark.asyncio
    async def test_consecutive_day_increments_streak(self, mock_user):
        """Activity on consecutive day should increment streak."""
        yesterday = date.today() - timedelta(days=1)
        mock_user.last_activity_date = yesterday
        mock_user.current_streak = 3
        mock_user.longest_streak = 3

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert mock_user.current_streak == 4
        assert mock_user.last_activity_date == date.today()

    @pytest.mark.asyncio
    async def test_streak_broken_resets_to_one(self, mock_user):
        """Activity after gap should reset streak to 1."""
        two_days_ago = date.today() - timedelta(days=2)
        mock_user.last_activity_date = two_days_ago
        mock_user.current_streak = 10
        mock_user.longest_streak = 10

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert mock_user.current_streak == 1
        assert mock_user.last_activity_date == date.today()

    @pytest.mark.asyncio
    async def test_longest_streak_not_decreased(self, mock_user):
        """Longest streak should never decrease."""
        yesterday = date.today() - timedelta(days=1)
        mock_user.last_activity_date = yesterday
        mock_user.current_streak = 3
        mock_user.longest_streak = 10

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert mock_user.longest_streak == 10

    @pytest.mark.asyncio
    async def test_longest_streak_updated_when_exceeded(self, mock_user):
        """Longest streak should update when current exceeds it."""
        yesterday = date.today() - timedelta(days=1)
        mock_user.last_activity_date = yesterday
        mock_user.current_streak = 5
        mock_user.longest_streak = 5

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert mock_user.longest_streak == 6

    @pytest.mark.asyncio
    async def test_first_app_badge_awarded_on_first_application(self, mock_user):
        """first_app badge should be awarded when total_apps becomes 1."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        mock_app = MagicMock()
        mock_app.final_outcome = None
        mock_app.stages = []

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([mock_app]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "first_app" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_streak_3_badge_awarded_at_3_days(self, mock_user):
        """streak_3 badge should be awarded when streak reaches 3."""
        yesterday = date.today() - timedelta(days=1)
        mock_user.last_activity_date = yesterday
        mock_user.current_streak = 2
        mock_user.longest_streak = 2
        mock_user.earned_badges = {}

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "streak_3" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_streak_7_badge_awarded_at_7_days(self, mock_user):
        """streak_7 badge should be awarded when streak reaches 7."""
        yesterday = date.today() - timedelta(days=1)
        mock_user.last_activity_date = yesterday
        mock_user.current_streak = 6
        mock_user.longest_streak = 6
        mock_user.earned_badges = {}

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "streak_7" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_streak_14_badge_awarded_at_14_days(self, mock_user):
        """streak_14 badge should be awarded when streak reaches 14."""
        yesterday = date.today() - timedelta(days=1)
        mock_user.last_activity_date = yesterday
        mock_user.current_streak = 13
        mock_user.longest_streak = 13
        mock_user.earned_badges = {}

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "streak_14" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_badge_not_awarded_twice(self, mock_user):
        """Already earned badge should not be awarded again."""
        already_earned_time = "2024-01-01T00:00:00"
        mock_user.last_activity_date = None
        mock_user.earned_badges = {"first_app": already_earned_time}

        mock_app = MagicMock()
        mock_app.final_outcome = None
        mock_app.stages = []

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([mock_app]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        # Badge should still have original timestamp
        assert mock_user.earned_badges["first_app"] == already_earned_time

    @pytest.mark.asyncio
    async def test_apps_5_badge_awarded_at_5_applications(self, mock_user):
        """apps_5 badge should be awarded when user has 5 applications."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        mock_apps = [MagicMock(final_outcome=None, stages=[]) for _ in range(5)]

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result(mock_apps),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "apps_5" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_apps_10_badge_awarded_at_10_applications(self, mock_user):
        """apps_10 badge should be awarded when user has 10 applications."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        mock_apps = [MagicMock(final_outcome=None, stages=[]) for _ in range(10)]

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result(mock_apps),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "apps_10" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_first_outcome_badge_awarded_when_outcome_logged(self, mock_user):
        """first_outcome badge should be awarded when an application has final_outcome."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        mock_app = MagicMock()
        mock_app.final_outcome = "rejected"
        mock_app.stages = []

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([mock_app]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "first_outcome" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_response_received_badge_awarded_when_response_stage(self, mock_user):
        """response_received badge should be awarded when an application has response stage."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        mock_app = MagicMock()
        mock_app.final_outcome = None
        mock_app.stages = [{"stage_type": "response"}]

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([mock_app]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "response_received" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_interview_1_badge_awarded_when_interview_stage(self, mock_user):
        """interview_1 badge should be awarded when an application has interview stage."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        mock_app = MagicMock()
        mock_app.final_outcome = None
        mock_app.stages = [{"stage_type": "interview"}]

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([mock_app]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert "interview_1" in mock_user.earned_badges

    @pytest.mark.asyncio
    async def test_user_not_found_returns_early(self):
        """Should return early if user is not found."""
        db = AsyncMock()
        user_result = MagicMock()
        user_result.scalar_one_or_none.return_value = None
        db.execute.return_value = user_result

        # Should not raise and should not commit
        await _update_gamification_on_activity(db, uuid4())
        db.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_earned_badges_persisted_to_user(self, mock_user):
        """Earned badges should be persisted to user.earned_badges."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = {}

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert isinstance(mock_user.earned_badges, dict)

    @pytest.mark.asyncio
    async def test_legacy_list_format_converted_to_dict(self, mock_user):
        """Legacy list format earned_badges should be converted to dict."""
        mock_user.last_activity_date = None
        mock_user.earned_badges = ["first_app", "streak_3"]  # legacy list

        db = AsyncMock()
        db.execute.side_effect = [
            self._make_user_result(mock_user),
            self._make_apps_result([]),
        ]

        await _update_gamification_on_activity(db, mock_user.id)

        assert isinstance(mock_user.earned_badges, dict)


class TestBadgeDefinitionModel:
    """BadgeDefinition Pydantic model tests."""

    def test_badge_definition_required_fields(self):
        """BadgeDefinition should require id, name, description, icon, earned."""
        badge = BadgeDefinition(
            id="test_badge",
            name="Test Badge",
            description="A test badge",
            icon="🏅",
            earned=False,
        )
        assert badge.id == "test_badge"
        assert badge.name == "Test Badge"
        assert badge.description == "A test badge"
        assert badge.icon == "🏅"
        assert badge.earned is False
        assert badge.earned_at is None

    def test_badge_definition_optional_earned_at(self):
        """earned_at should be optional and default to None."""
        badge = BadgeDefinition(
            id="test_badge",
            name="Test Badge",
            description="A test badge",
            icon="🏅",
            earned=True,
            earned_at="2024-03-15T10:30:00",
        )
        assert badge.earned_at == "2024-03-15T10:30:00"

    def test_badge_definition_iso_string_earned_at(self):
        """earned_at should accept ISO format string."""
        badge = BadgeDefinition(
            id="test_badge",
            name="Test Badge",
            description="A test badge",
            icon="🏅",
            earned=True,
            earned_at=datetime.now().isoformat(),
        )
        assert badge.earned_at is not None
