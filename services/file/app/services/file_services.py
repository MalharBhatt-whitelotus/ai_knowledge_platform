import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException, status

from services.file.app.storage.local_storage import StorageProvider
from services.file.app.repositories.file_repository import FileRepository


class FileServices:

    def __init__(self, repository: FileRepository, storage_provider: StorageProvider, publisher):
        self.repository = repository
        self.storage_provider = storage_provider
        self.publisher = publisher