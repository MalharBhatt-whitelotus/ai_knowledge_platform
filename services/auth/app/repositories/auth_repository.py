from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.app.models.auth_models import UserAuthenticationDetail
from services.auth.app.schemas.auth_schemas import RegisterRequest, RegisterResponse


class AuthRepository:


    """
    ---------------------------------------
            * Search Username Function *
    ---------------------------------------
    """
    async def search_username(username: str, db: AsyncSession) -> RegisterResponse:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.username == username))
        user = result.scalar_one_or_none()
        return user


    """
    ---------------------------------------
            * Search Email Function *
    ---------------------------------------
    """
    async def search_email(email: str, db: AsyncSession) -> RegisterResponse:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.email == email))
        user = result.scalar_one_or_none()
        return True if user else False


    """
    ---------------------------------------
            * Register User Function *
    ---------------------------------------
    """    
    async def register_user(
            user_credentials: RegisterRequest,
            user_id: str, 
            hashed_password: str,
            created_at: datetime,
            updated_at: datetime,
            db: AsyncSession
            ) -> RegisterResponse:
        
        user = UserAuthenticationDetail(
            user_id = user_id,
            first_name = user_credentials.first_name,
            last_name = user_credentials.last_name,
            email = user_credentials.email,
            username = user_credentials.username,
            password_hash = hashed_password,
            role = user_credentials.role,
            is_active = False,
            is_verified = False,
            created_at = created_at,
            updated_at = updated_at,
            #new_column
            doc_id = user_credentials.doc_id,
            doc_type = user_credentials.doc_type
        )

        await db.execute(select(UserAuthenticationDetail))
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user


    """
    ---------------------------------------
      * Update User Activation Function *
    ---------------------------------------
    """
    async def update_user_active(username: str, is_active: bool, db: AsyncSession) -> bool:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.username == username))
        user = result.scalar_one_or_none()
        user.is_active = is_active

        await db.commit()
        await db.refresh(user)

        return user.is_active


    """
    ---------------------------------------
     * Update User Verification Function *
    ---------------------------------------
    """
    async def update_user_verify(username: str, is_verified: bool, db: AsyncSession) -> bool:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.username == username))
        user = result.scalar_one_or_none()
        user.is_verified = is_verified

        await db.commit()
        await db.refresh(user)

        return user.is_verified


    """
    ---------------------------------------
     * Update Time Function *
    ---------------------------------------
    """
    async def updated_at(username: str, time: datetime, db: AsyncSession) -> datetime:
        result = await db.execute(select(UserAuthenticationDetail).where(UserAuthenticationDetail.username == username))
        user = result.scalar_one_or_none()
        user.updated_at = time

        await db.commit()
        await db.refresh(user)

        return time


    """
    ---------------------------------------
            * Rollback Function *
    ---------------------------------------
    """
    async def rollback(db: AsyncSession):
        await db.rollback()