from pydantic import BaseModel, ConfigDict
from services.file.app.enums import Role

class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    username: str
    email: str
    role: Role
    is_active: bool
    is_verify: bool