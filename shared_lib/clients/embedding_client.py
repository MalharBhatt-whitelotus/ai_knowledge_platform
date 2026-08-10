import httpx

from shared_lib.config.settings import settings
from shared_lib.retry.decorators import http_retry

class EmbeddingClient:


    def __init__(self):
        self.base_url = settings.EMBEDDING_URL


    @http_retry
    async def generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/internal/generate_embeddings",
                    json={"chunks":chunks}
                    )

                if response.status_code >= 400:
                    print(
                        "Embedding Service Error:",
                        response.status_code,
                        response.text,
                        )

                response.raise_for_status()
                return response.json()