from fastapi import APIRouter, Request, status, Depends

from services.embedding.app.services.embedding_services import EmbeddingService
from services.embedding.app.schemas.embedding_schema import EmbeddingRequest, EmbeddingResponse

embedding_router = APIRouter()

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

@embedding_router.post("/internal/generate_embeddings", response_model=EmbeddingResponse, status_code=status.HTTP_200_OK)
async def generate_embeddings(
    request: EmbeddingRequest,
    services: EmbeddingService = Depends(get_embedding_service)
    ):
    embeddings = await services.generate_embeddings(request)

    return EmbeddingResponse(embeddings=embeddings)