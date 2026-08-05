from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile

from shared_lib.enums import DocStatus, DocType

class FileResponse(BaseModel):
    file_id: str
    owner_id: str
    original_filename: str
    content_type: DocType
    file_size: int
    status: DocStatus
    created_at: datetime
    updated_at: datetime