from fastapi import status, HTTPException

from services.ai.app.clients.genai_client import GenaiClient
from services.ai.app.clients.search_client import SearchClient
from services.ai.app.services.prompt_builder import PromptBuilder
from services.ai.app.schemas.ai_schemas import AskAIRequest, AskAIResponse


class AIService:


    def __init__(
            self, 
            genai_client: GenaiClient,
            search_client: SearchClient,
            prompt_builder: PromptBuilder,
            ) -> None:
        self.ai_client = genai_client
        self.search_client = search_client
        self.prompt_builder = prompt_builder


    async def ask(self, request: AskAIRequest):
        try:
            search_results = await self.search_client.search(request.question, request.top_k)
            if not search_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search Results not found.")
            print(f">>> {search_results}")
            
            prompt =  self.prompt_builder.build(question=request.question, chunks=search_results.get("chunks"),)
            if not prompt:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")
            print(f">>> {prompt}")
            
            answer = await self.ai_client.generate(prompt=prompt)
            if not answer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
            print(f">>> {answer}")
            
            return AskAIResponse(question=request.question, answer=answer,)

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(exc)}")