import uuid

class ChromaRepository:

    def __init__(self, collection):
        self.collection = collection

    async def add(self, file_id: str, owner_id: str, chunks: list[str], embeddings: list[list[float]]) -> None:
        ids = [str(uuid.uuid4) for _ in chunks]
        metadatas = [
            {
                "file_id": file_id,
                "owner_id": owner_id,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            chunks=chunks,
            metadatas=metadatas
        )
