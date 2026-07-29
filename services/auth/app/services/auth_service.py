from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from services.auth.app.security.jwt import JWTManager
from services.auth.app.utils.auth_utils import AuthUtils as utils
from services.auth.app.repositories.auth_repository import AuthRepository as repo
from services.auth.app.schemas.auth_schemas import RegisterRequest, RegisterResponse, AuthRequest, AuthResponse, TokenResponse


class AuthService:


    async def register_user(user_credentials: RegisterRequest, db: AsyncSession) -> RegisterResponse:
        try:
            if await repo.search_username(user_credentials.username, db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")

            if await repo.search_email(user_credentials.email, db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

            if not utils.check_password(user_credentials.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User Credentials")

            if user_credentials.role is not "user":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")

            user_uuid = utils.get_uuid()
            hashed_password = utils.hash_password(user_credentials.password)
            created_at = datetime.now(timezone.utc)
            updated_at = datetime.now(timezone.utc)

            registered_user = await repo.register_user(user_credentials, user_uuid, hashed_password, created_at, updated_at, db)
            if not registered_user:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="User not registered.")

            return registered_user
            
        except HTTPException:
            await repo.rollback(db)
            raise

        except Exception as exc:
            await repo.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


    async def login_user(user_credentials: AuthRequest, db: AsyncSession) -> AuthResponse:
        try:
            if not await repo.search_username(user_credentials.username, db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

            if not utils.check_password(user_credentials.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials.")

            user_password = utils.hash_password(user_credentials.password)
            if user_password is await repo.get_password(user_credentials.username, db):
                access_token = JWTManager.create_access_token(user_password)
                refresh_token = JWTManager.create_refresh_token(user_password)
                username = await repo.user_is_active(username, db)

                return AuthResponse(
                    username=username, 
                    token=TokenResponse(
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_type="Bearer"
                        )
                    )
            else :
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detial="Wrong user credentials.")

        except HTTPException:
            await repo.rollback(db)
            raise

        except Exception as exc:
            await repo.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Error.")