from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.search.app.services import service
from services.search.app.schemas.search_schemas import StoreEmbeddingRequest, StoreEmbeddingResponse, AskQuestionRequest, AskQuestionResponse


search_router = APIRouter()


@search_router.post("/internal/store_embedding", response_model=StoreEmbeddingResponse, status_code=status.HTTP_200_OK)
async def store_embeddings(request: StoreEmbeddingRequest):

    response = await service.store_embeddings(request)

    return response


@search_router.post("/ask", response_model=AskQuestionResponse, status_code=status.HTTP_200_OK)
async def ask_question(request: AskQuestionRequest):
    response = await service.ask_question(request)
    return response