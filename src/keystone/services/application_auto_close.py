"""Auto-close stale applications that have had no status update in 60 days.

Runs as a daily Celery Beat task to close applications where:
- Status is not already terminal (REJECTED, WITHDRAWN, CLOSED)
- last_activity_at is older than 60 days (or created_at if never updated)
"""
import structlog
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.base import async_session_factory
from keystone.models.entities import Application, ApplicationStatus

logger = structlog.get_logger()

STALE_DAYS = 60


class ApplicationAutoClose:
    """Auto-close stale applications after 60 days of inactivity."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def close_stale_applications(self, stale_days: int = STALE_DAYS) -> dict:
        """Close applications with no activity for the specified number of days.

        Args:
            stale_days: Number of days of inactivity before auto-close (default 60)

        Returns:
            Stats dict with counts of closed applications
        """
        logger.info("application_auto_close.start", stale_days=stale_days)

        start_time = datetime.utcnow()
        cutoff = datetime.utcnow() - timedelta(days=stale_days)

        # Terminal statuses that should not be auto-closed
        terminal_statuses = [
            ApplicationStatus.REJECTED,
            ApplicationStatus.WITHDRAWN,
            ApplicationStatus.CLOSED,
        ]

        # Find stale applications:
        # - Status is not terminal
        # - No activity for stale_days (last_activity_at < cutoff)
        # - Not already auto-closed
        query = select(Application).where(
            and_(
                Application.status.notin_(terminal_statuses),
                Application.auto_closed_at.is_(None),
                # Either last_activity_at is old, or created_at if last_activity_at is null
                (
                    Application.last_activity_at < cutoff
                ) | (
                    (Application.last_activity_at.is_(None)) &
                    (Application.created_at < cutoff)
                ),
            )
        )

        result = await self.session.execute(query)
        stale_apps = result.scalars().all()

        closed_count = 0
        for app in stale_apps:
            app.status = ApplicationStatus.CLOSED
            app.auto_closed_at = datetime.utcnow()
            app.updated_at = datetime.utcnow()
            closed_count += 1
            logger.info(
                "application.auto_closed",
                application_id=str(app.id),
                employer=app.employer,
                role=app.role,
                days_inactive=(
                    (datetime.utcnow() - app.last_activity_at).days
                    if app.last_activity_at
                    else (datetime.utcnow() - app.created_at).days
                ),
            )

        await self.session.commit()

        duration = (datetime.utcnow() - start_time).total_seconds()
        stats = {
            "stale_apps_found": len(stale_apps),
            "applications_closed": closed_count,
            "duration_seconds": duration,
        }

        logger.info("application_auto_close.complete", stats=stats)
        return stats


async def close_stale_applications_task(stale_days: Optional[int] = None) -> dict:
    """Convenience function to run auto-close task.

    Called by Celery Beat schedule or manually via API.
    """
    days = stale_days if stale_days is not None else STALE_DAYS
    async with async_session_factory() as session:
        auto_close = ApplicationAutoClose(session)
        return await auto_close.close_stale_applications(stale_days=days)


# ---------------------------------------------------------------------------
# Celery task registration
# ---------------------------------------------------------------------------
from celery import Task


class _ApplicationAutoCloseTask(Task):
    """Celery-bound wrapper for ApplicationAutoClose.close_stale_applications."""

    name = "keystone.services.application_auto_close.close_stale_applications"

    def run(self, stale_days: Optional[int] = None) -> dict:
        """Synchronous entry point required by Celery executor.

        Runs the auto-close inside an async session and returns the stats dict.
        """
        import asyncio
        return asyncio.run(close_stale_applications_task(stale_days=stale_days))


close_stale_applications_task = _ApplicationAutoCloseTask()
