import httpx
from fastapi import HTTPException, status

from shared_lib.logger.logger import get_logger
from shared_lib.retry.decorators import http_retry


class SearchClient:


    def __init__(self):
        self.base_url = "http://search_service:8004"
        self.logger = get_logger(__name__)


    @http_retry
    async def store_vectors(self, file_id: str, owner_id: str, chunks: list[str], embeddings: list[list[float]]):
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/internal/store_embedding",
                    json={
                        "file_id": file_id,
                        "owner_id": owner_id,
                        "chunks": chunks,
                        "embeddings": embeddings,
                        }
                )

                if response.status_code != status.HTTP_200_OK:
                    raise HTTPException(
                        status_code=response.status_code, 
                        detail=response.json().get("detail")
                        )

                return response.json()

            except HTTPException as exc:
                self.logger.error(">>> %s", exc)
                raise

            except httpx.RequestError as r_exc:
                self.logger.error(">>> %s", r_exc)
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Search Service unavailble.>>> {r_exc}")