from datetime import datetime, timezone
from fastapi import APIRouter, Request
from shared_lib.schemas.health import HealthResponse
from shared_lib.config.settings import settings

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
    return {
        "status": "ready",
        "service": request.app.title,
    }