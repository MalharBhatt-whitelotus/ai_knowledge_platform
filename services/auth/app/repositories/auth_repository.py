from sqlalchemy import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.app.models.auth_models import UserAuthenticationDetail
from services.auth.app.schemas.auth_schemas import RegisterRequest, RegisterResponse

class AuthRepository:

    async def search_username(username: str, db: AsyncSession) -> RegisterResponse:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.username == username))
        user = result.scalar_one_or_none()
        return True if user else False

    async def search_email(email: str, db: AsyncSession) -> RegisterResponse:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.email == email))
        user = result.scalar_one_or_none()
        return True if user else False
    
    async def register_user(
            user_credentials: RegisterRequest,
            uuid: str, 
            hashed_password: str,
            created_at: datetime,
            updated_at: datetime,
            db: AsyncSession
            ) -> RegisterResponse:
        
        user = UserAuthenticationDetail(
            uuid = uuid,
            first_name = user_credentials.first_name,
            last_name = user_credentials.last_name,
            email = user_credentials.email,
            username = user_credentials.username,
            password_hash = hashed_password,
            role = user_credentials.role,
            is_active = False,
            is_verified = False,
            created_at = created_at,
            updated_at = updated_at
        )

        await db.execute(select(UserAuthenticationDetail))
        await db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def get_password(username, db):
        ...

    async def user_is_active(username, db):
        ...

    async def rollback(db: AsyncSession):
        await db.execute(select(UserAuthenticationDetail))
        await db.rollback()