from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, requests,status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from shared_lib.config.settings import settings
from shared_lib.schemas.health import HealthResponse

from services.auth.app.database.auth_database import get_db
from services.auth.app.config.settings import settings as auth_settings
from services.auth.app.services.auth_service import AuthService as service
from services.auth.app.dependencies.current_user import get_current_user
from services.auth.app.schemas.auth_schemas import RegisterRequest,RegisterResponse, AuthRequest, AuthResponse, CurrentUserResponse, UserLogoutResponse


router = APIRouter()


@router.get("/health")
async def health():
    return HealthResponse(service=auth_settings.SERVICE_NAME, status="ok", version=settings.APP_VERSION, timestamp=datetime.now(timezone.utc))


@router.post("/register_user",response_model=RegisterResponse, status_code=status.HTTP_201_CREATED,)
async def register_user(user_credentials: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await service.register_user(user_credentials, db)
    return result


@router.post("/login_user", response_model=AuthResponse, status_code=200)
async def login_user(user_credentials: AuthRequest, db: AsyncSession = Depends(get_db)):
    result = await service.login_user(user_credentials, db)
    return result

@router.post("/logout_user", response_model=UserLogoutResponse, status_code=200)
async def logout_user(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await service.logout_user(current_user, db)
    return result
    
@router.post("/me", response_model=CurrentUserResponse, status_code=200)
async def current_user(current_user = Depends(get_current_user)):
    return current_user