import httpx
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from shared_lib.schemas.current_user import CurrentUserResponse

security = HTTPBearer()

class AuthClient:

    def __init__(self, ):
        self.base_url = "http://auth_service:8001"


    async def __call__(self, authorization: HTTPAuthorizationCredentials = Depends(security),) -> CurrentUserResponse:
        try:
            token = authorization.credentials
            headers = {
                "Authorization": f"Bearer {token}"
                }
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/me",
                    headers=headers
                )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json()["detail"],
                )

            print(response.json())
            return CurrentUserResponse(**response.json())

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Auth Service unavailable.",
            )


auth_client = AuthClient()