from fastapi import HTTPException, status

from services.search.app.schemas.search_schemas import StoreEmbeddingRequest, StoreEmbeddingResponse, AskQuestionRequest, AskQuestionResponse, RetrivedChunks


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


    async def ask_question(self, request: AskQuestionRequest) -> AskQuestionResponse:
        try:
            query_embedding = await self.embedding.generate_embeddings(list(request.question))
            if not query_embedding:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No relevent data found.")

            search_results = await self.repo.search(
                embeddings=query_embedding.get("embeddings"),
                top_k=request.top_k
                )
            if not search_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No relevant files found.")

            result = [
                RetrivedChunks(
                    content=result.get("file"),
                    metadatas=result.get("metadata"),
                    score=result.get("score"),
                    )
                    for result in search_results
                ]
            if not result:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Unable to generate result.")

            return AskQuestionResponse(
                question=request.question,
                chunks=result
            )

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(exc)
                )