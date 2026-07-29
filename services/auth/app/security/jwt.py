from typing import Any
from jose import JWTError, jwt
from datetime import UTC, datetime, timedelta

from services.auth.app.config.settings import settings
class JWTManager:
    """Utility class for creating and verifying JWT tokens."""

    @staticmethod
    def generate_tokens(user) -> tuple[str, str]:

        access_token = JWTManager.create_access_token(
            data={
                "sub": user.username,
                "email": user.email,
                "role": user.role
                }
        )

        refresh_token = JWTManager.create_refresh_token(
            data={
                "sub": user.username
            }
        )

        return access_token, refresh_token
    
    @staticmethod
    def create_access_token(data: dict[str, Any]) -> str:
        payload = data.copy()

        now = datetime.now(UTC)

        payload.update(
            {
                "iat": now,
                "exp": now + timedelta(
                    minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
                ),
                "type": "access",
            }
        )

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHMS,
        )

    @staticmethod
    def create_refresh_token(data: dict[str, Any]) -> str:
        payload = data.copy()

        now = datetime.now(UTC)

        payload.update(
            {
                "iat": now,
                "exp": now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
                "type": "refresh",
            }
        )

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHMS   
        )

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHMS]
        )

    @staticmethod
    def verify_access_token(token: str) -> dict[str, Any]:
        payload = JWTManager.decode_token(token)

        if payload.get("type") != "access":
            raise JWTError("Invalid token type.")

        return payload

    @staticmethod
    def verify_refresh_token(token: str) -> dict[str, Any]:
        payload = JWTManager.decode_token(token)

        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type.")

        return payload