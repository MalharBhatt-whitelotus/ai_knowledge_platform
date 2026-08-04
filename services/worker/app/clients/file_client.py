import httpx
from fastapi import HTTPException, status

from services.worker.app.schemas.file_client_schemas import FileResponse

class FileClient:


    def __init__(self):
        self.Base_url = "http://file_service:8002"


    async def get_file(
            self, 
            file_id: str,
            ) -> FileResponse:
        try: 
            async with httpx.AsyncClient(timeout=10.0) as client:
                response =  await client.get(
                    f"{self.Base_url}/internal/get_file/{file_id}",
                    )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])
            
            return FileResponse.model_validate(response.json())
        
        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="File Service unavailable")

        except HTTPException:
            raise


    async def download_file(self, file_id: str) -> bytes:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.Base_url}/internal/download_file/{file_id}")

                if response.status_code != status.HTTP_200_OK:
                    raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])

                return response.content
            
        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="File service unavailable.")

        except HTTPException:
            raise


    async def extract_text(self, file_id: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.Base_url}/internal/extract_text/{file_id}")
                if response.status_code != status.HTTP_200_OK:
                    raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])

                return response.text

        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="File Service Unavailable.")

        except HTTPException:
             raise

    async def update_status(self, file_id: str, status: str):
        ...