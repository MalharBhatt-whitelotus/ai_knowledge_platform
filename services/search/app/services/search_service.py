from fastapi import HTTPException, status

from services.search.app.schemas.search_schemas import StoreEmbeddingRequest, StoreEmbeddingResponse, AskQuestionRequest, AskQuestionResponse


class SearchService:
    def __init__(self, repo, embedding_client) -> None:
        self.repo = repo
        self.embedding = embedding_client

    async def store_embeddings(self, request: StoreEmbeddingRequest) -> StoreEmbeddingResponse:
        try:
            await self.repo.add(
                file_id = request.file_id, 
                owner_id=request.owner_id,
                chunks=request.chunks,
                embeddings=request.embeddings
                )

            return StoreEmbeddingResponse(
                success=True,
                message="Embedding stored successfully.",
                file_id=request.file_id,
                chunks_stored=len(request.chunks)
            )

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to store embeddings: {exc}",
            )

    async def ask_service(self, request: AskQuestionRequest) -> AskQuestionResponse:
        # Step 1
        # Generate query embedding

        # Step 2
        # Search ChromaDB

        # Step 3
        # Convert response

        ...