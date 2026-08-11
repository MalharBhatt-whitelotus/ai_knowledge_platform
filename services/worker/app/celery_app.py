from celery import Celery
from celery.schedules import crontab

from shared_lib.config.settings import settings

celery_app = Celery("worker_service", broker=settings.CELERY_BROKER_URL,backend=settings.CELERY_RESULT_BACKEND,)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_cancel_long_running_tasks_on_connection_loss=True,

    imports= [
        "services.worker.app.tasks.cleanup_task",
    ],
)
celery_app.conf.beat_schedule = {
    "run-cleanup-every-10-minutes": {
        "task": "services.worker.app.tasks.cleanup_task.cleanup_task",
        "schedule": 600.0,
    },
}