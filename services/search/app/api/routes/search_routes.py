from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.logger.logger import get_logger

from services.search.app.schemas.search_schemas import StoreEmbeddingRequest, StoreEmbeddingResponse
from services.search.app.services.search_service import SearchService as service
from services.search.app.database.search_database import get_db

search_router = APIRouter()

logger = get_logger(__name__)

@search_router.post("/internal/store_embedding", response_model=StoreEmbeddingResponse, status_code=status.HTTP_200_OK)
async def store_embeddings(request: StoreEmbeddingRequest, db: AsyncSession = Depends(get_db)):

    response = await service.store_embeddings(request, db)

    return response