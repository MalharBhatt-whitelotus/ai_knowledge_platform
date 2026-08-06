import uuid

class ChromaRepository:


    def __init__(self, collection):
        self.collection = collection


    async def add(self, file_id: str, owner_id: str, chunks: list[str], embeddings: list[list[float]]) -> None:
        ids = [str(uuid.uuid4()) for _ in chunks]
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
            documents=chunks,
            metadatas=metadatas
        )


    async def search(self, embeddings: list[list[float]], top_k:int) -> list[dict]:
        results = self.collection.query(
            query_embeddings=embeddings,
            n_results = top_k,
        )

        files = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        return [{
            "id": doc_id,
            "file": file,
            "metadata": metadata,
            "score": distance,
        }
        for doc_id, file, metadata, distance in zip(ids, files, metadatas, distances)
        ]