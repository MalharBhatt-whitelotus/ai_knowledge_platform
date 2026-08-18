from celery import Celery
from celery.schedules import crontab
from kombu import Queue

from shared_lib.config.settings import settings


celery_app = Celery(
    "worker_service",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    timezone="UTC",
    enable_utc=True,

    worker_enable_remote_control=False,
    worker_cancel_long_running_tasks_on_connection_loss=True,

    imports=[
        "services.worker.app.tasks.cleanup_task",
    ],

    # Explicitly define a durable Celery queue
    task_queues=(
        Queue(
            "celery",
            durable=True,
        ),
    ),

    task_default_queue="celery",
    task_default_exchange="celery",
    task_default_exchange_type="direct",
    task_default_routing_key="celery",
)


celery_app.conf.beat_schedule = {
    "run-cleanup-every-10-minutes": {
        "task": "services.worker.app.tasks.cleanup_task.cleanup_task",
        "schedule": 600.0,
    },
}