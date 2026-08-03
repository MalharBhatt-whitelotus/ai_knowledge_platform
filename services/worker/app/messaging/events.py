from uuid import UUID
from pydantic import BaseModel

class FileUploadedEvent(BaseModel):
    file_id: UUID
    owner_id: UUID
    storage_path: str
    content_type: str