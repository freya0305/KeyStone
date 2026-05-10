"""Scheduled Celery tasks for KeyStone ETL pipeline.

- Nightly ETL: runs at 00:00 SGT (16:00 UTC) daily
- Full rebuild: runs every 7 days
"""
import structlog
from datetime import timedelta

from celery.schedules import crontab

from keystone.workers.celery_app import celery_app
from keystone.services.skill_etl import SkillETL, run_etl_for_tuple
from keystone.models.base import async_session_factory

logger = structlog.get_logger()


@celery_app.task(bind=True, name="keystone.etl.nightly")
def nightly_etl(self):
    """Nightly ETL task - runs at 00:00 SGT (16:00 UTC) daily.

    Performs incremental skill frequency update for all active JDs.
    Full rebuild is triggered separately every 7 days.
    """
    logger.info("celery.nightly_etl.start")

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            etl = SkillETL(session)
            return await etl.run_nightly_etl()

    try:
        result = asyncio.run(_run())
        logger.info("celery.nightly_etl.complete", stats=result)
        return result
    except Exception as e:
        logger.exception("celery.nightly_etl.failed", error=str(e))
        raise


@celery_app.task(bind=True, name="keystone.etl.full_rebuild")
def full_rebuild_etl(self):
    """Full rebuild ETL task - runs every 7 days.

    Drops and recomputes all skill frequency data from scratch.
    Use for complete data refresh or recovery from data corruption.
    """
    logger.info("celery.full_rebuild_etl.start")

    import asyncio

    async def _run():
        async with async_session_factory() as session:
            etl = SkillETL(session)
            # Full rebuild: process all JDs without filtering
            return await etl.run_nightly_etl()

    try:
        result = asyncio.run(_run())
        logger.info("celery.full_rebuild_etl.complete", stats=result)
        return result
    except Exception as e:
        logger.exception("celery.full_rebuild_etl.failed", error=str(e))
        raise


# Celery Beat schedule configuration
celery_app.conf.beat_schedule = {
    "nightly-etl-0000-sgt": {
        "task": "keystone.etl.nightly",
        # 00:00 SGT (Singapore Time, UTC+8) = 16:00 UTC
        "schedule": crontab(hour=16, minute=0),
    },
    "full-rebuild-every-7-days": {
        "task": "keystone.etl.full_rebuild",
        # Every 7 days
        "schedule": timedelta(days=7),
    },
}
