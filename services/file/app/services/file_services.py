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
             * Init Function * 
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
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))