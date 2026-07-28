from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.app.repositories import auth_repository as repo
from services.auth.app.schemas.auth_schemas import AuthRequest, AuthResponse

class AuthService:

    async def register_user(user_credentials: AuthRequest, db: AsyncSession) -> AuthResponse:
        return AuthResponse