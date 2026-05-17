"""Celery application configuration for KeyStone ETL workers."""
from celery import Celery
from celery.schedules import crontab

from keystone.core import get_settings
from keystone.services.skill_etl import run_nightly_etl_task
from keystone.services.application_auto_close import close_stale_applications_task

settings = get_settings()

celery_app = Celery(
    "keystone",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    task_soft_time_limit=3300,  # 55 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# Celery Beat schedules
celery_app.conf.beat_schedule = {
    "nightly-skill-etl": {
        "task": "keystone.services.skill_etl.run_nightly_etl",
        "schedule": crontab(minute=0, hour=16),  # 00:00 SGT (UTC+8) = 16:00 UTC
        "kwargs": {},
    },
    "daily-auto-close-stale": {
        "task": "keystone.services.application_auto_close.close_stale_applications",
        "schedule": crontab(minute=0, hour=16),  # 00:00 SGT (UTC+8) = 16:00 UTC
        "kwargs": {"stale_days": 60},
    },
}
