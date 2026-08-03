from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.auth.app.security.jwt import JWTManager
from services.auth.app.database.auth_database import get_db as db
from services.auth.app.schemas.auth_schemas import  CurrentUserResponse
from services.auth.app.repositories.user_repository import UserRepository as repo

security = HTTPBearer()

async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(db)) -> CurrentUserResponse:
    try:
        if not authorization:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access is not allowed.")

        schemes = authorization.scheme
        token = authorization.credentials
        if not token or not schemes:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access.")
        
        payload = JWTManager.verify_access_token(token) 
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized Access")

        username = payload["sub"]
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized access")

        user = await repo.get_user_by_username(username, db)
        if not user or user.is_active == False or user.is_verified == False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")

        return CurrentUserResponse(user_id=user.user_id, username=user.username, email=user.email, role=user.role, is_active=user.is_active, is_verify=user.is_verified)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))