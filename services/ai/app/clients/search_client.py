import httpx
from fastapi import HTTPException, status


class SearchClient:


    def __init__(self):
        self.base_url = "http://search_service:8004"


    async def search(self, question: str, top_k: int):
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/ask",
                    json={
                        "question": question,
                        "top_k": top_k,
                    }
                    )

                if response.status_code != status.HTTP_200_OK:
                    raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

                return response.json()

            except HTTPException:
                raise

            except httpx.RequestError as r_exc:
                raise HTTPException(status_code=status.HTTP_200_OK, detail=f"Search service unavailable: {str(r_exc)}")