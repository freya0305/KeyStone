"""Celery application configuration for KeyStone ETL workers."""
from celery import Celery
from keystone.core import get_settings

settings = get_settings()

celery_app = Celery(
    "keystone",
    broker=f"{settings.redis_url}/0",
    backend=f"{settings.redis_url}/0",
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
