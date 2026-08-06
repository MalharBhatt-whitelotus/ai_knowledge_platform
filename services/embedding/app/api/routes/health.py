from fastapi import APIRouter
from datetime import datetime, timezone

from shared_lib.config.settings import settings
from shared_lib.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    return HealthResponse(
        service="Embedding",
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.now(timezone.utc)
    )