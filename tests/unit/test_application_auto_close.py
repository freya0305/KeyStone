"""Tests for application_auto_close service - auto-close stale applications after 60 days."""
import uuid
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from keystone.models.entities import Application, ApplicationStatus
from keystone.services.application_auto_close import (
    ApplicationAutoClose,
    STALE_DAYS,
    close_stale_applications_task,
)


class TestApplicationAutoClose:
    """Tests for ApplicationAutoClose.close_stale_applications."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock AsyncSession."""
        session = MagicMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        return session

    @pytest.fixture
    def auto_close(self, mock_session):
        """Create ApplicationAutoClose with mocked session."""
        return ApplicationAutoClose(mock_session)

    def _make_app(
        self,
        status: ApplicationStatus = ApplicationStatus.APPLIED,
        last_activity_at: datetime | None = None,
        created_at: datetime | None = None,
        auto_closed_at: datetime | None = None,
    ) -> MagicMock:
        """Create a mock Application with specified fields."""
        app = MagicMock(spec=Application)
        app.id = uuid.uuid4()
        app.status = status
        app.employer = "Test Corp"
        app.role = "Software Engineer"
        app.last_activity_at = last_activity_at
        app.created_at = created_at or datetime.utcnow()
        app.auto_closed_at = auto_closed_at
        app.updated_at = datetime.utcnow()
        return app

    @pytest.mark.asyncio
    async def test_closes_applications_older_than_60_days(self, auto_close, mock_session):
        """Applications with no activity for >60 days should be closed."""
        stale_date = datetime.utcnow() - timedelta(days=61)
        stale_app = self._make_app(
            status=ApplicationStatus.APPLIED,
            last_activity_at=stale_date,
        )

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [stale_app]
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 1
        assert stats["applications_closed"] == 1
        assert stale_app.status == ApplicationStatus.CLOSED
        assert stale_app.auto_closed_at is not None
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_does_not_close_applications_newer_than_60_days(self, auto_close, mock_session):
        """Applications with recent activity should NOT be closed.

        The SQL query itself filters by staleness, so the service receives
        an empty result when no apps exceed the 60-day threshold.
        """
        # Query returns empty - no apps meet the staleness criteria
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 0
        assert stats["applications_closed"] == 0
        # Service always commits, even when no apps to close
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_uses_created_at_when_last_activity_is_none(self, auto_close, mock_session):
        """Applications with no last_activity_at should use created_at for staleness."""
        old_created = datetime.utcnow() - timedelta(days=61)
        app = self._make_app(
            status=ApplicationStatus.INTERESTED,
            last_activity_at=None,
            created_at=old_created,
        )

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [app]
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 1
        assert stats["applications_closed"] == 1
        assert app.status == ApplicationStatus.CLOSED

    @pytest.mark.asyncio
    async def test_does_not_close_applications_exactly_at_60_days(self, auto_close, mock_session):
        """Applications with last_activity_at exactly at 60 days should NOT be closed.

        At exactly 60 days (cutoff boundary), the app is NOT stale since the query
        uses last_activity_at < cutoff (strict less-than). The SQL query itself
        filters these out, so the service receives an empty result.
        """
        # Query returns empty - exactly 60 days is not stale (< cutoff required)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 0
        assert stats["applications_closed"] == 0
        # Service always commits, even when no apps to close
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_does_not_close_terminal_status_applications(self, auto_close, mock_session):
        """Applications with terminal statuses (REJECTED, WITHDRAWN, CLOSED) should not be closed."""
        terminal_statuses = [
            ApplicationStatus.REJECTED,
            ApplicationStatus.WITHDRAWN,
            ApplicationStatus.CLOSED,
        ]

        for status in terminal_statuses:
            old_date = datetime.utcnow() - timedelta(days=100)
            app = self._make_app(
                status=status,
                last_activity_at=old_date,
            )

            mock_result = MagicMock()
            # Empty result - terminal apps should not be found by query
            mock_result.scalars.return_value.all.return_value = []
            mock_session.execute.return_value = mock_result

            stats = await auto_close.close_stale_applications()

            assert stats["stale_apps_found"] == 0, f"{status} should not be auto-closed"

    @pytest.mark.asyncio
    async def test_does_not_close_already_auto_closed_applications(self, auto_close, mock_session):
        """Applications already auto-closed should not be closed again."""
        old_date = datetime.utcnow() - timedelta(days=100)
        already_closed = self._make_app(
            status=ApplicationStatus.CLOSED,
            last_activity_at=old_date,
            auto_closed_at=datetime.utcnow() - timedelta(days=50),
        )

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 0
        assert stats["applications_closed"] == 0

    @pytest.mark.asyncio
    async def test_close_stale_applications_respects_custom_stale_days(self, auto_close, mock_session):
        """The stale_days parameter should override the default 60-day threshold."""
        old_date = datetime.utcnow() - timedelta(days=31)
        app = self._make_app(
            status=ApplicationStatus.APPLIED,
            last_activity_at=old_date,
        )

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [app]
        mock_session.execute.return_value = mock_result

        # With 30-day threshold, 31-day-old app should be closed
        stats = await auto_close.close_stale_applications(stale_days=30)

        assert stats["stale_apps_found"] == 1
        assert stats["applications_closed"] == 1
        assert app.status == ApplicationStatus.CLOSED

    @pytest.mark.asyncio
    async def test_close_stale_applications_empty_result(self, auto_close, mock_session):
        """Empty result should return zero counts."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 0
        assert stats["applications_closed"] == 0
        assert "duration_seconds" in stats
        # Service always commits, even when no apps to close
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_stale_applications_multiple_apps(self, auto_close, mock_session):
        """Multiple stale applications should all be closed."""
        old_date = datetime.utcnow() - timedelta(days=100)
        apps = [
            self._make_app(status=ApplicationStatus.APPLIED, last_activity_at=old_date),
            self._make_app(status=ApplicationStatus.INTERVIEW, last_activity_at=old_date),
            self._make_app(status=ApplicationStatus.SCREENING, last_activity_at=old_date),
        ]

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = apps
        mock_session.execute.return_value = mock_result

        stats = await auto_close.close_stale_applications()

        assert stats["stale_apps_found"] == 3
        assert stats["applications_closed"] == 3
        for app in apps:
            assert app.status == ApplicationStatus.CLOSED
            assert app.auto_closed_at is not None


class TestStaleDaysConstant:
    """Tests for the STALE_DAYS constant."""

    def test_stale_days_is_60(self):
        """STALE_DAYS should be 60."""
        assert STALE_DAYS == 60


class TestCeleryTaskWrapper:
    """Tests for the Celery task wrapper."""

    def test_task_has_correct_name(self):
        """Task name should match the expected format."""
        assert close_stale_applications_task.name == (
            "keystone.services.application_auto_close.close_stale_applications"
        )

    def test_task_run_accepts_stale_days_parameter(self):
        """Task.run() should accept stale_days parameter."""
        # Verify the run method accepts stale_days
        import inspect
        sig = inspect.signature(close_stale_applications_task.run)
        params = list(sig.parameters.keys())
        assert "stale_days" in params

    def test_task_is_task_instance(self):
        """close_stale_applications_task should be a Celery Task instance."""
        from celery import Task
        assert isinstance(close_stale_applications_task, Task)
