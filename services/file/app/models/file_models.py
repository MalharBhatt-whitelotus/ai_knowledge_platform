import enum
from sqlalchemy import Column, String, Integer, DateTime, Enum, Boolean

from services.file.app.config.settings import settings

class DocType(enum.Enum):
    pdf = "pdf"
    txt = "txt"
    docx = "docx"
    xlsx = "xlsx"
    pptx = "pptx"

class File:

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, nullable=False, index=True)
    original_filename = Column(String, nullable=False, index=True)
    stored_filename = Column(String, nullable=False, index=True, unique=True)
    content_type = Column(Enum(DocType), nullable=False, default=DocType.txt)
    file_size = Column(...)
    ...