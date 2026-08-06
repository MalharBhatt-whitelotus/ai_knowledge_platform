from fastapi import status, HTTPException

from services.ai.app.schemas.ai_schemas import AskAIRequest, AskAIResponse
from services.ai.app.clients.search_client import SearchClient
from services.ai.app.clients.openai_client import OpenaiClient
from services.ai.app.services.prompt_builder import PromptBuilder


class AIService:


    def __init__(
            self, 
            search_client: SearchClient,
            prompt_builder: PromptBuilder,
            openai_client: OpenaiClient,
            ) -> None:
        self.ai_client = openai_client
        self.search_client = search_client
        self.prompt_builder = prompt_builder


    async def ask(self, request: AskAIRequest):
        try:
            search_results = await self.search_client.search(request.question, request.top_k)
            if not search_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search Results not found.")
            
            prompt = await self.prompt_builder.build(question=request.question, chunks=search_results.chunks,)
            if not prompt:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")
            
            answer = await self.ai_client.generate(prompt=prompt)
            if not answer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")

            return AskAIResponse(question=request.question, answer=answer,)

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(exc)}")