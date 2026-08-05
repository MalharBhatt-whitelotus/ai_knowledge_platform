from fastapi import APIRouter, status

from services.embedding.app.services import embedding_service as services
from services.embedding.app.schemas.embedding_schema import EmbeddingRequest, EmbeddingResponse

embedding_router = APIRouter()

@embedding_router.post("/internal/generate_embeddings", response_model=EmbeddingResponse, status_code=status.HTTP_200_OK)
async def generate_embeddings(
    request: EmbeddingRequest,
    ):
    embeddings = await services.generate_embeddings(request.chunks)

    return EmbeddingResponse(embeddings=embeddings)