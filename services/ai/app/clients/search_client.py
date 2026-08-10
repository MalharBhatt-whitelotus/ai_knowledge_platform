import httpx

from shared_lib.retry.decorators import http_retry


class SearchClient:


    def __init__(self):
        self.base_url = "http://search_service:8004"


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