from fastapi import APIRouter

from shared_lib.config.settings import settings
from shared_lib.schemas.health import HealthResponse

router = APIRouter()

@router.get("/health",response_model=HealthResponse)
async def health():
    return HealthResponse(
        service="Gateway Service",
        status="healthy",
        version=settings.APP_VERSION,
    )