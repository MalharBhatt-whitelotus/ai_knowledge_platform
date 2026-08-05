from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    chunks: list[str]

class EmbeddingResponse(BaseModel):
    embeddings: list[list[float]]