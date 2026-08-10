import uuid
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException, status

from shared_lib.logger.logger import get_logger
from shared_lib.enums import DocStatus

from services.worker.app.messaging.events import FileUploadedEvent
from services.worker.app.messaging.publisher import RabbitMQPublisher

from services.file.app.parser.parser_factory import ParserFactory
from services.file.app.storage.storage_provider import StorageProvider
from services.file.app.repositories.file_repository import FileRepository as repo
from services.file.app.schemas.file_schemas import FileUploadResponse, FileResponse


class FileServices:


    """
    -------------------------------------
             * Init Function * 
    -------------------------------------
    """
    #  
    def __init__(self, repository: repo, storage_provider: StorageProvider, publisher : RabbitMQPublisher):
        self.repository = repository
        self.storage_provider = storage_provider
        self.publisher = publisher
        self.logger = get_logger(__name__)


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

            file_path = await self.storage_provider.save(upload_file, stored_filename)
            if not file_path:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="File not saved.")

            file_size = upload_file.size
            if not file_size or file_size <= 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid file size.")
            
            file = await self.repository.create_file(
                file_id = str(file_id), 
                owner_id = user_id,
                original_filename = str(title),
                stored_filename = stored_filename,
                content_type = extension[1::],
                file_size = file_size,
                storage_path = file_path,
                status = DocStatus.in_queue,
                created_at = datetime.now(timezone.utc),
                updated_at = datetime.now(timezone.utc),
                db = db
                )
            if not file:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="File not saved.")

            event = FileUploadedEvent(
                file_id=str(file_id),
                owner_id= user_id,
                storage_path=file_path,
                content_type=extension[1::],
            )

            self.logger.info(">>> Publishing FileUploadedEvent...")
            await self.publisher.publish_file_uploaded(event=event)

            return file

        except HTTPException:
            await self.repository.rollback(db)
            await self.storage_provider.delete(file_path)
            raise

        except Exception as exc:
            await self.repository.rollback(db)
            await self.storage_provider.delete(file_path)
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

            await self.repository.delete(file.file_id, db)
            await self.storage_provider.delete(file.storage_path)
            
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
    async def download_file(self, file_id: str, db: AsyncSession) -> bytes:
        try:
            file_path = await self.repository.get_file_path_by_file_id(file_id, db)
            if not file_path:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            if not self.storage_provider.exists(file_path):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            downloaded_file = await self.storage_provider.download(file_path)
            if not downloaded_file:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File not downloaded.")

            return downloaded_file

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


    """
    -------------------------------------
       * Get File By FileID Function * 
    -------------------------------------
    """    
    async def get_file_by_file_id(self, file_id: str, user_id: str, db: AsyncSession) -> FileResponse:
        try:
            file = await self.repository.get_by_file_id(file_id, db)
            if not file:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            if file.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access.")
            
            return FileResponse(
                file_id=file.file_id,
                owner_id=file.owner_id,
                original_filename=file.original_filename,
                content_type=file.content_type,
                file_size=file.file_size,
                status=file.status,
                created_at=file.created_at,
                updated_at=file.updated_at
            )

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))
    """
    -------------------------------------
       * Get Internal File Function * 
    -------------------------------------
    """    
    async def get_internal_file(self, file_id: str, db: AsyncSession) -> FileResponse:
        try:
            file = await self.repository.get_by_file_id(file_id, db)
            if not file:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
            
            return FileResponse(
                file_id=file.file_id,
                owner_id=file.owner_id,
                original_filename=file.original_filename,
                content_type=file.content_type,
                file_size=file.file_size,
                status=file.status,
                created_at=file.created_at,
                updated_at=file.updated_at
            )

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))

    """
    -------------------------------------
        * Get File Bytes Function * 
    -------------------------------------
    """ 
    async def get_file_bytes(self, file_id: str, db: AsyncSession) -> bytes:
        try:
            file_path = await self.repository.get_file_path_by_file_id(file_id, db)
            
            if not file_path:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

            if not await self.storage_provider.exists(file_path):
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
            
            file_bytes = await self.storage_provider.download(file_path)

            if not file_bytes:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="File not available.")

            return file_bytes

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


    """
    -------------------------------------
          * Extract Text Function * 
    -------------------------------------
    """ 
    async def extract_text(self, file_id: str, db: AsyncSession) -> str:
        try:
            file_details = await self.repository.get_by_file_id(file_id, db)
            if not file_details:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            content_type = file_details.content_type

            parser = ParserFactory.get_parser(content_type.value)

            file_path = await self.repository.get_file_path_by_file_id(file_id, db)
            if not file_path:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            text = await parser.extract_text(file_path)
            if not text or not text.strip():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No text could be extracted.")

            return text

        except HTTPException:
            raise

        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=str(exc))
        
        except Exception as exc:
            self.logger.error(">>> %s", str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


    """
    -------------------------------------
          * Status Update Function * 
    -------------------------------------
    """ 
    async def status_update(self, file_id: str, updated_status: DocStatus, db: AsyncSession) -> str:
        try:
            if not await self.repository.get_by_file_id(file_id, db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

            response =  await self.repository.update_status(file_id, updated_status, db)
            if not response:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="File status not updated.")

            return response
        
        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))