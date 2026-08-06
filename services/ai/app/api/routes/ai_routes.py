from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from services.ai.app.services import service
from services.ai.app.schemas.ai_schemas import AskAIRequest, AskAIResponse

ai_router = APIRouter()

@ai_router.post("/ask", response_model=AskAIResponse, status_code=status.HTTP_200_OK)
async def ask_ai(request: AskAIRequest):

    response = await service.ask(request)

    return response

@ai_router.post("/ai/stream",response_model=AskAIResponse, status_code=status.HTTP_200_OK)
async def stream_ai(request: AskAIRequest):
    generator = await service.stream(request=request)

    return StreamingResponse(content=generator, media_type="text/plain")