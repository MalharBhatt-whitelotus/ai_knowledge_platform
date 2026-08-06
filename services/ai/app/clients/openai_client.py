import httpx
from fastapi import HTTPException, status

from services.ai.app.config.setting import settings

class OpenaiClient:


    def __init__(self) -> None:
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"

    async def generate(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/responses",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.OPENAI_MODEL,
                        "input": prompt,
                    }
                    )

                response.raise_for_status()

                data = response.json()

                return data["output"][0]["context"][0]["text"]

        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=exc.response.json().get("error",{}).get(
                "message","OpenAI API error."
            ),
            )            

        except httpx.RequestError as r_exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Open ai service is unavailable : {str(r_exc)}")