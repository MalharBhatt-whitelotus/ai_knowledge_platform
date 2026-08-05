import httpx
from fastapi import HTTPException, status


class EmbeddingClient:


    def __init__(self):
        self.base_url = "http://embedding_service:8003"


    async def generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/internal/generate_embeddings",
                    json={"chunks":chunks}
                    )

                if response.status_code != status.HTTP_200_OK:
                    raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", response.text))

                return response.json()
            
            except HTTPException:
                raise

            except httpx.RequestError as exc:
                raise(HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)))