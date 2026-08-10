import httpx

from shared_lib.retry.decorators import http_retry
from services.worker.app.schemas.file_client_schemas import FileResponse


class FileClient:


    def __init__(self):
        self.Base_url = "http://file_service:8002"


    @http_retry
    async def get_file(
            self, 
            file_id: str,
            ) -> FileResponse:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response =  await client.get(
                    f"{self.Base_url}/internal/get_file/{file_id}",
                    )

            response.raise_for_status()
            
            return FileResponse.model_validate(response.json())


    @http_retry
    async def download_file(self, file_id: str) -> bytes:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.Base_url}/internal/download_file/{file_id}"
                )

            response.raise_for_status()

        return response.content


    @http_retry
    async def extract_text(self, file_id: str) -> str:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                      f"{self.Base_url}/internal/extract_text/{file_id}"
                      )

                response.raise_for_status()

                return response.text


    @http_retry        
    async def update_status(self, file_id: str, status_update: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
                respone = await client.post(
                    f"{self.Base_url}/internal/status_update/{file_id}",
                    params={"status":status_update},
                    )

                respone.raise_for_status()

                return respone.json()