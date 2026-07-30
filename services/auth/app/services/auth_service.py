from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.app.security.jwt import JWTManager
from services.auth.app.utils.auth_utils import AuthUtils as utils
from services.auth.app.repositories.auth_repository import AuthRepository as repo
from services.auth.app.schemas.auth_schemas import RegisterRequest, RegisterResponse, AuthRequest, AuthResponse, TokenResponse


class AuthService:


    """
    ---------------------------------------
          * Register User Function *
    ---------------------------------------
    """
    async def register_user(user_credentials: RegisterRequest, db: AsyncSession) -> RegisterResponse:
        try:
            if await repo.search_username(user_credentials.username, db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")

            if await repo.search_email(user_credentials.email, db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

            if not utils.check_password(user_credentials.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User Credentials")

            user_id = str(utils.get_uuid())
            hashed_password = utils.hash_password(user_credentials.password)
            created_at = datetime.now(timezone.utc)
            updated_at = datetime.now(timezone.utc)

            registered_user = await repo.register_user(user_credentials, user_id, hashed_password, created_at, updated_at, db)
            if not registered_user:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="User not registered.")

            return registered_user
            
        except HTTPException:
            await repo.rollback(db)
            raise

        except Exception as exc:
            await repo.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


    """
    ---------------------------------------
            * Login User Function *
    ---------------------------------------
    """
    async def login_user(user_credentials: AuthRequest, db: AsyncSession) -> AuthResponse:
        try:
            if not utils.check_password(user_credentials.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials.")

            user = await repo.search_username(user_credentials.username, db)

            if not user or not utils.verify_password(user_credentials.password, user.password_hash):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
            
            access_token, refresh_token = JWTManager.generate_tokens(user)
            if not access_token or not refresh_token:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generated the authentication token")

            is_active = await repo.update_user_active(user.username, db)
            is_verify = await repo.update_user_verify(user.username, db)
            if not is_active or not is_verify:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed to login user.")
            now = datetime.now(timezone.utc)

            time = await repo.updated_at(user.username, now, db)
            if not time:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed to Update.")
            
            return AuthResponse(
                    username=user.username, 
                    token=TokenResponse(
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_type="Bearer"
                        ),
                    is_active=is_active,
                    is_verify=is_verify
                    )            

        except HTTPException:
            await repo.rollback(db)
            raise

        except Exception as exc:
            await repo.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    """
    ---------------------------------------
            * Login User Function *
    ---------------------------------------
    """
    async def logout_user(user_credentials: AuthRequest, db: AsyncSession) -> AuthResponse:
        ...