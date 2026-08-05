from pydantic import BaseModel

class StoreEmbeddingRequest(BaseModel):
    file_id: str
    owner_id: str
    chunks: list[str]
    embeddings: list[list[float]]

class StoreEmbeddingResponse(BaseModel):
    success: bool
    message: str
    file_id: str
    chunks_stored: int