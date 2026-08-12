from prometheus_client import Counter, Histogram


CELERY_TASK_COUNT = Counter(
    "celery_tasks_total",
    "Total number of Celery tasks",
    ["task", "status"],
)

CELERY_TASK_DURATION = Histogram(
    "celery_task_duration_seconds",
    "Celery task execution duration",
    ["task"],
)