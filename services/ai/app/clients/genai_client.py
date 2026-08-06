import httpx
from google import genai
from google.genai import errors, types
from fastapi import HTTPException, status
from collections.abc import AsyncGenerator

from services.ai.app.config.setting import settings

class GenaiClient:


    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GENAI_API_KEY)


    async def generate(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=10.0):
               response = await self.client.aio.models.generate_content(
                model=settings.GENAI_MODEL,  # e.g., "gemini-2.5-flash"
                contents=prompt,
            )

            if not response.text:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Gemini returned an empty response.",
                )

            return response.text

        except errors.APIError as exc:
            raise HTTPException(
                status_code=exc.code or status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"GenAI API error: {exc.message}",
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"GenAI service is unavailable: {str(exc)}",
            )


    async def stream_generate(self, prompt: str) -> AsyncGenerator[str, None]:
            async with httpx.AsyncClient(timeout=10.0):
                response_stream = await self.client.aio.models.generate_content_stream(
                    model=settings.GENAI_MODEL,
                    contents=prompt,
                    config={"temperature": 0,},
                )

                async for chunk in response_stream:
                    token = chunk.text
                    if token:
                        yield token