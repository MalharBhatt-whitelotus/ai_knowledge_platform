from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.search.app.schemas.search_schemas import StoreEmbeddingRequest, StoreEmbeddingResponse
from services.search.app.services.search_service import SearchService as service

search_router = APIRouter()

@search_router.post("/internal/store_embedding", response_model=StoreEmbeddingResponse, status_code=status.HTTP_200_OK)
async def store_embeddings(request: StoreEmbeddingRequest):

    response = await service.store_embeddings(request)

    return response