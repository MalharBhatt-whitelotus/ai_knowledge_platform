from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.search.app.schemas.search_schemas import StoreEmbeddingRequest
class SearchService:
    async def store_embeddings(request: StoreEmbeddingRequest, db: AsyncSession):
        ...