from sqlalchemy import Column, String, Integer, DateTime, Enum, Boolean

from services.file.app.config.settings import settings
from services.file.app.enums import DocType, DocStatus


class File:

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, nullable=False, index=True)
    owner_id = Column(String, nullable=False, index=True)
    original_filename = Column(String, nullable=False, index=True)
    stored_filename = Column(String, nullable=False, index=True, unique=True)
    content_type = Column(Enum(DocType), default=DocType.txt)
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String, nullable=False, unique=True)
    status = Column(Enum(DocStatus), default=DocStatus.in_queue)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)