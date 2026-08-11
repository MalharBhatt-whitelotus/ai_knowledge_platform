from services.worker.app.celery_app import celery_app

@celery_app.task
def cleanup_task():
    print("Running cleanup task")

    return {
        "status": "completed"
    }