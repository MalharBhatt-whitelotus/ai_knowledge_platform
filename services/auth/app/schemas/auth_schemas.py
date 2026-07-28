from datetime import datetime
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_tname: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=15)
    role: str = Field(default="user")
    
    
class RegisterResponse(BaseModel):
    id: int
    uuid: str
    first_name: str
    last_name: str
    email: str
    username: str
    password_hash: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class AuthRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=15)


class AuthResponse(BaseModel):
    username: str
    access_token: str
    request_token: str