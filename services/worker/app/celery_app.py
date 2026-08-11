from celery import Celery

from shared_lib.config.settings import settings

celery_app = Celery("worker_service", broker=settings.CELERY_BROKER_URL,backend=settings.CELERY_RESULT_BACKEND,)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)