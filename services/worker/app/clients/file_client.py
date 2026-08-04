import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


class FileClient:


    def __init__(self):
        self.Base_url = "http://file:8002"


    async def get_file(
            self, 
            file_id: str, 
            authorization: HTTPAuthorizationCredentials = Depends(security)
            ):
        token = authorization.credentials
        headers = {
            "Authorization": f"Bearer {token}"
        }

        async with httpx.AsyncClient as client:
           response =  await client.get(f"{self.Base_url}/get_file/{file_id}", headers=headers)

           if response.status_code != status.HTTP_200_OK:
               raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])
        
           return response


    async def download_file(self, file_id: str):
        ...

    async def update_status(self, file_id: str, status: str):
        ...