class EmbeddingService:

    async def generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        ...