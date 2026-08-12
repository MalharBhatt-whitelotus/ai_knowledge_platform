from datetime import datetime, timezone
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from shared_lib.config.settings import settings
from shared_lib.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model= HealthResponse)
async def health(request: Request):
    return HealthResponse(
        service= request.app.title, 
        status="Healthy", 
        version=settings.APP_VERSION, 
        timestamp=datetime.now(timezone.utc)
        )


@router.get("/ready")
async def readiness(request: Request):
    checks = {}

    redis_client = getattr(request.app.state, "redis", None)

    if redis_client:
        try:
            await redis_client.client.ping()

            checks["redis"] = "healthy"

        except Exception:
            checks["redis"] = "unhealthy"

    status = ("ready" if all(value == "healthy" for value in checks.values()) else "not_ready")

    status_code = (200 if status == "ready" else 503)

    return JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "service": request.app.title,
            "checks": checks,
        }
    )