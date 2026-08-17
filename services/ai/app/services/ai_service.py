from fastapi import status, HTTPException
from fastapi.responses import StreamingResponse

from shared_lib.clients.search_client import SearchClient

from services.ai.app.services.cache_key import CacheKey
from services.ai.app.clients.genai_client import GenaiClient
from services.ai.app.services.cache_service import CacheService
from services.ai.app.services.prompt_builder import PromptBuilder
from services.ai.app.schemas.ai_schemas import AskAIRequest, AskAIResponse


class AIService:


    def __init__(
            self, 
            genai_client: GenaiClient,
            search_client: SearchClient,
            prompt_builder: PromptBuilder,
            cache_service: CacheService,
            ) -> None:
        self.ai_client = genai_client
        self.search_client = search_client
        self.prompt_builder = prompt_builder
        self.cache_service = cache_service


    async def ask(self, request: AskAIRequest):
        try:
            search_results = await self.search_client.search(request.question, request.top_k)
            if not search_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search Results not found.")
            print(f">>> {search_results}")

            cache_key = CacheKey.generate(chunks=search_results.get("chunks"), question=request.question)

            cache_answer = await self.cache_service.get(key=cache_key)
            if cache_answer is not None:
                print(">>> Cache answer hit...")
                return AskAIResponse(question=request.question, answer=cache_answer)
            
            prompt =  self.prompt_builder.build(question=request.question, chunks=search_results.get("chunks"),)
            if not prompt:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")
            print(f">>> {prompt}")
            
            answer = await self.ai_client.generate(prompt=prompt)
            if not answer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
            print(f">>> {answer}")

            await self.cache_service.set(key=cache_key, value=answer)
            print(">>> Answer is cached...")
            
            return AskAIResponse(question=request.question, answer=answer,)

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(exc)}")
        
    async def stream(self, request: AskAIRequest):
        try:
            search_results = await self.search_client.search(request.question, request.top_k)
            if not search_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search Results not found.")
            print(f">>> {search_results}")

            cache_key = CacheKey.generate(chunks=search_results.get("chunks"), question=request.question)
            cache_answer = await self.cache_service.get(key=cache_key)
            if cache_answer is not None:
                print(">>> Cache answer hit...")
                async def cached_generator():
                    yield cache_answer
                return cached_generator()
            
            prompt =  self.prompt_builder.build(question=request.question, chunks=search_results.get("chunks"),)
            if not prompt:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")
            print(f">>> {prompt}")
            
            answer = self.ai_client.stream_generate(prompt=prompt)
            if not answer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
            print(f">>> {answer}")

            async def generate_and_cache():
                chunks = []
                async for chunk in answer:
                    chunks.append(chunk)
                    yield chunk
                complete_answer = "".join(chunks)
                await self.cache_service.set(
                    key=cache_key,
                    value=complete_answer,
                )
                print(">>> Answer is cached...")
            return generate_and_cache()

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(exc)}")