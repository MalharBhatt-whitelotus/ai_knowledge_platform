import uuid
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException, status

from services.file.app.enums import DocStatus
from services.file.app.storage.storage_provider import StorageProvider
from services.file.app.repositories.file_repository import FileRepository
from services.file.app.schemas.file_schemas import FileRequest, FileUploadResponse
class FileServices:


    """
    -------------------------------------
             * Init Function * 
    -------------------------------------
    """
    def __init__(self, repository: FileRepository, storage_provider: StorageProvider, publisher):
        self.repository = repository
        self.storage_provider = storage_provider
        self.publisher = publisher


    """
    -------------------------------------
           * Upload File Function * 
    -------------------------------------
    """
    async def upload_file(self, upload_file: UploadFile, user_id: str, db: AsyncSession) -> FileUploadResponse:
        try:
            title = Path(upload_file.filename)
            extension = title.suffix
            file_id = uuid.uuid4()
            stored_filename = f"{file_id}{extension}"

            file_path = self.storage_provider.save(file, stored_filename)
            if not file_path:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="File not saved.")

            file_size = file.size
            if not file_size or file_size <= 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid file size.")
            
            file = await self.repository.create_file(
                file_id = file_id, 
                owner_id = user_id,
                stored_filename = stored_filename,
                content_type = extension[1::],
                file_size = file_size,
                storage_path = file_path,
                status = DocStatus.in_queue,
                created_at = datetime.now(timezone.utc),
                updated_at = datetime.now(timezone.utc),
                file_details = FileRequest(title=title),
                db = db
                )
            if not file:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="File not saved.")

            await self.publisher.publish_file_uploaded(file.file_id)

            return file

        except HTTPException:
            await self.repository.rollback(db)
            raise

        except Exception as exc:
            await self.repository.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))


    """
    -------------------------------------
           * Delete File Function * 
    -------------------------------------
    """
    async def delete_file(self, file_id: str, db: AsyncSession) -> None:
        try:
            file = await self.repository.get_by_file_id(file_id, db)
            if file is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            if not self.storage_provider.exists(file.storage_path):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            await self.storage_provider.delete(file.storage_path)
            await self.repository.delete(file.file_id, db)
            
        except HTTPException:
            await self.repository.rollback(db)
            raise

        except Exception as exc:
            await self.repository.rollback(db)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


    """
    -------------------------------------
           * Download File Function * 
    -------------------------------------
    """
    async def download_file(self, file_id: str, db: AsyncSession) -> UploadFile:
        try:
            file = self.repository.get_by_file_id(file_id, db)
            if not file:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            if not self.storage_provider.exists(file.storage_path):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            downloaded_file = self.storage_provider.download(file.storage_path)
            if not downloaded_file:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File not downloaded.")

            return downloaded_file

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")