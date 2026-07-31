from datetime import datetime
from pydantic import BaseModel

from services.file.app.enums import DocType, DocStatus

class FileRequest(BaseModel):
    title: str
    description: str | None = None

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    status: DocStatus
    message: str

class FileResponse(BaseModel):
    file_id: str
    owner_id: str
    original_filename: str
    content_type: DocType
    file_size: int
    status: DocStatus
    created_at: datetime
    updated_at: datetime

class FileListResponse(BaseModel):
    files: list[FileResponse]
    totel: int
    page: int
    page_size: int