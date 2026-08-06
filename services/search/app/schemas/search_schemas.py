from pydantic import BaseModel, Field


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


class AskQuestionRequest(BaseModel):
    question: str = Field(min_lenght=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrivedChunks(BaseModel):
    content: str
    score: float
    metadatas: dict


class AskQuestionResponse(BaseModel):
    question: str
    chunks: list[RetrivedChunks]