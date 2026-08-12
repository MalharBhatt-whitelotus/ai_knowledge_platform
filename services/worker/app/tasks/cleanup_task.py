import time

from services.worker.app.celery_app import celery_app

from shared_lib.logger.logger import get_logger
from services.worker.app.metrics import CELERY_TASK_COUNT, CELERY_TASK_DURATION


logger = get_logger(__name__)

@celery_app.task
def cleanup_task():

    start = time.perf_counter()

    task_name = cleanup_task.name

    try:

        logger.info("Starting Celery task: %s", task_name)

        result = {"status": "completed"}

        CELERY_TASK_COUNT.labels(
            task = task_name,
            status = "success",
        ).inc()

        return result

    except Exception:

        CELERY_TASK_COUNT.labels(
            task = task_name,
            status = "failure",
            ).inc()

        logger.exception(
            "Celery task failed: %s",
            task_name,
        )

        raise

    finally:

        duration = (time.perf_counter() - start)

        CELERY_TASK_DURATION.labels(
            task=task_name,
        ).observe(duration)

        logger.info(
            "Celery task finished: %s | %.2f ms",
            task_name,
            duration * 1000
        )