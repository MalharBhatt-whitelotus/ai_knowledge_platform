from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from services.file.app.enums import  DocType, DocStatus
from services.file.app.models.file_models import File
from services.file.app.schemas.file_schemas import FileRequest, FileResponse


class FileRepository:


    """
    --------------------------------------------
               * Creat File Function *
    --------------------------------------------
    """
    async def create_file(
            file_id: str,
            owner_id: str,
            stored_filename: str,
            content_type: DocType,
            file_size: int,
            storage_path: str,
            status: DocStatus,
            created_at: datetime,
            updated_at: datetime,
            file_details: FileRequest, 
            db: AsyncSession
            ) -> FileResponse:

        
        file = File(
            file_id = file_id,
            owner_id = owner_id,
            original_filename = file_details.title,
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