from pydantic import BaseModel

class FileUploadedEvent(BaseModel):
    file_id: str
    owner_id: str
    storage_path: str
    content_type: str