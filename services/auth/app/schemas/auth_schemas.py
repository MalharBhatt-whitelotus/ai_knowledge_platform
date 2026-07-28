from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=15)

class AuthResponse(BaseModel):
    username: str
    access_token: str
    request_token: str