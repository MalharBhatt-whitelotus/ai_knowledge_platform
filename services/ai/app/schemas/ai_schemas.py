from pydantic import BaseModel, Field

class AskAIRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, lt=20)

class AskAIResponse(BaseModel):
    question: str
    answer: str