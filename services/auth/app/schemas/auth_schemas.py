from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from services.auth.app.enums import Role, DocType


class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=15)
    role: Role = Role.user
    
class RegisterResponse(BaseModel):
    id: int
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password_hash: str
    role: Role
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class AuthRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=15)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class AuthResponse(BaseModel):
    username: str
    token: TokenResponse
    is_active: bool
    is_verify: bool


class UserLogoutResponse(BaseModel):
    username: str
    is_active: bool
    updated_at: datetime

class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    username: str
    email: str
    role: Role
    is_active: bool
    is_verify: bool