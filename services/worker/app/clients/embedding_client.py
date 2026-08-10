import httpx

from shared_lib.retry.decorators import http_retry


class EmbeddingClient:


    def __init__(self):
        self.base_url = "http://embedding_service:8003"


    @http_retry
    async def generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/internal/generate_embeddings",
                    json={"chunks":chunks}
                    )

                response.raise_for_status()
                return response.json()