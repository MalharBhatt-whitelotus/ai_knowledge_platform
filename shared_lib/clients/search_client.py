import httpx

from shared_lib.config.settings import settings
from shared_lib.retry.decorators import http_retry


class SearchClient:


    def __init__(self):
        self.base_url = settings.SEARCH_URL


    @http_retry
    async def store_vectors(self, file_id: str, owner_id: str, chunks: list[str], embeddings: list[list[float]]):
        async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/internal/store_embedding",
                    json={
                        "file_id": file_id,
                        "owner_id": owner_id,
                        "chunks": chunks,
                        "embeddings": embeddings,
                        }
                )

                response.raise_for_status()
                return response.json()


    @http_retry
    async def search(self, question: str, top_k: int):
        async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/ask",
                    json={
                        "question": question,
                        "top_k": top_k,
                    }
                    )

                response.raise_for_status()

                return response.json()