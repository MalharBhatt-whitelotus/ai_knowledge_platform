from pydantic import BaseModel

class ErrorDetail(BaseModel):
    code: str
    message: str
    service: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail