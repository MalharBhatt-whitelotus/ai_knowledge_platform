import httpx
from fastapi import HTTPException, status
from services.file.app.schemas.auth_schemas import CurrentUserResponse

class AuthClient:

    def __init__(self):
        self.base_url = "http://auth_service:8001"

    async def get_current_user(self) -> CurrentUserResponse:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/me"
                )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json()["detail"],
                )

            return CurrentUserResponse(**response.json())

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Auth Service unavailable.",
            )


auth_client = AuthClient()