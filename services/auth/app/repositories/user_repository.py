from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.app.schemas.auth_schemas import RegisterResponse
from services.auth.app.models.auth_models import UserAuthenticationDetail


class UserRepository:


    async def get_user_by_username(username: str, db: AsyncSession) -> RegisterResponse:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.username == username))
        user = result.scalar_one_or_none()
        return user