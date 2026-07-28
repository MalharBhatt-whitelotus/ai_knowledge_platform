from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from services.auth.app.utils.auth_utils import AuthUtils as utils
from services.auth.app.repositories.auth_repository import AuthRepository as repo
from services.auth.app.schemas.auth_schemas import RegisterRequest, RegisterResponse, AuthRequest, AuthResponse


class AuthService:


    async def register_user(user_credentials: RegisterRequest, db: AsyncSession) -> RegisterResponse:
        try:
            if await repo.search_username(user_credentials.username, db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")

            if await repo.search_email(user_credentials.email, db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

            if not utils.check_email(user_credentials.email):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email.")

            if not utils.check_password(user_credentials.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User Credentials")

            if user_credentials.role is not "user":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")

            hashed_password = utils.hash_password(user_credentials.password)
            registered_user = await repo.register_user(user_credentials, hashed_password, db)
            if not registered_user:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="User not registered.")

            return registered_user
            
        except HTTPException:
            await db.rollback(db)
            raise

        except Exception as exc:
            await db.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


    async def login_user(user_credentials: AuthRequest, db: AsyncSession) -> AuthResponse:
        try:
            if not await repo.search_username(user_credentials.username, db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            if not utils.check_password(user_credentials.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials.")
            user_password = utils.hash_password(user_credentials.password)
            if user_password is await repo.get_password(user_credentials.username, db):
                #go to the security section to generate token.
                ...
        except HTTPException:
            raise