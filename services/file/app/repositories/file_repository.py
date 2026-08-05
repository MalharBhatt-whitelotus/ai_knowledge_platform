from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from services.file.app.enums import  DocType, DocStatus
from services.file.app.models.file_models import File
from services.file.app.schemas.file_schemas import FileResponse, FileUploadResponse


class FileRepository:


    """
    --------------------------------------------
               * Creat File Function *
    --------------------------------------------
    """
    async def create_file(
            file_id: str,
            owner_id: str,
            original_filename: str, 
            stored_filename: str,
            content_type: DocType,
            file_size: int,
            storage_path: str,
            status: DocStatus,
            created_at: datetime,
            updated_at: datetime,
            db: AsyncSession
            ) -> FileUploadResponse:

        
        file = File(
            file_id = file_id,
            owner_id = owner_id,
            original_filename = original_filename,
            stored_filename = stored_filename,
            content_type = content_type,
            file_size = file_size,
            storage_path = storage_path,
            status = status,
            created_at = created_at,
            updated_at = updated_at
        )

        await db.execute(select(File))
        db.add(file)
        await db.commit()
        await db.refresh(file)

        return FileUploadResponse(
            file_id=file.file_id,
            filename=file.original_filename,
            status=file.status,
            message="File Uploaded Successfully."
            )

    
    """
    --------------------------------------------
               * Get By File ID Function *
    --------------------------------------------
    """
    async def get_by_file_id(file_id: str, db: AsyncSession) -> FileResponse:
        result = await db.execute(select(File).where(File.file_id == file_id))
        file = result.scalar_one_or_none()
        return  FileResponse(
            file_id=file.file_id,
            owner_id=file.owner_id,
            original_filename=file.original_filename,
            content_type=file.content_type,
            file_size=file.file_size,
            status=file.status,
            created_at=file.created_at,
            updated_at=file.updated_at
        )


    """
    --------------------------------------------
       * Get File Path By File ID Function *
    --------------------------------------------
    """
    async def get_file_path_by_file_id(file_id: str, db: AsyncSession) -> str:
        result = await db.execute(select(File).where(File.file_id == file_id))
        file_details = result.scalar_one_or_none()

        return file_details.storage_path 
    

    """
    --------------------------------------------
               * Get By File Name Function *
    --------------------------------------------
    """
    async def get_by_stored_filename(stored_filename: str, db: AsyncSession) -> FileResponse:
        result = await db.execute(select(File).where(
            File.stored_filename == stored_filename
            ))
        file = result.scalar_one_or_none()
        return  FileResponse(
            file_id=file.file_id,
            owner_id=file.owner_id,
            original_filename=file.original_filename,
            content_type=file.content_type,
            file_size=file.file_size,
            status=file.status,
            created_at=file.created_at,
            updated_at=file.updated_at
        )


    """
    --------------------------------------------
            * Delete File Function *
    --------------------------------------------
    """
    async def delete(file_id: str, db: AsyncSession) -> None:
        result = await db.execute(select(File).where(File.file_id == file_id))
        file = result.scalar_one_or_none()
        await db.delete(file)
        await db.commit()


    """
    --------------------------------------------
            * Update Status Function *
    --------------------------------------------
    """
    async def update_status(file_id: str, status: DocStatus, db: AsyncSession) -> str:
        result = await db.execute(select(File).where(File.file_id == file_id))
        file = result.scalar_one_or_none()
        file.status = status

        await db.commit()
        await db.refresh(file)

        return file.status.value


    """
    --------------------------------------------
            * Rollback DB Function *
    --------------------------------------------
    """
    async def rollback(db: AsyncSession):
        await db.rollback()

       
    """
    --------------------------------------------
               * Addition Suedo Function *
    --------------------------------------------
    """
    async def lists_documents():
        ...
    async def count():
        ...
    async def search():
        ...
    async def filter():
        ...
    async def get_by_owner():
        ...
    async def exists():
        ...