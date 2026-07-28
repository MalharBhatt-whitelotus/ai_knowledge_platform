from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, requests, Depends

from shared_lib.config.settings import settings
from shared_lib.schemas.health import HealthResponse

from services.auth.app.database.auth_database import get_db
from services.auth.app.services.auth_service import AuthService as service
from services.auth.app.config.settings import settings as auth_settings
from services.auth.app.schemas.auth_schemas import AuthRequest, AuthResponse


register_router = APIRouter()


@register_router.get("/healthy_register")
async def health():
    return HealthResponse(service=auth_settings.SERVICE_NAME, status="ok", version=settings.APP_VERSION, timestamp=datetime.now(timezone.utc))


@register_router.post("/register_user",response_model=AuthResponse)
async def register_user(user_credentials: AuthRequest, db: AsyncSession = Depends(get_db)):
    result = service.register_user(user_credentials, db)
    return result