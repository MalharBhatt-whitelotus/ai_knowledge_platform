from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,status,File,UploadFile, Depends

from services.file.app.database.file_database import get_db
from services.file.app.dependencies.file_dependency import get_file_service
from services.file.app.services.file_services import FileServices
from services.file.app.storage.storage_provider import StorageProvider
from services.file.app.schemas.file_schemas import FileResponse, FileUploadResponse

from services.file.app.dependencies.role_checker import user_only

file_router = APIRouter()

@file_router.post("/upload_file", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(user_only),                 
    services: FileServices = Depends(get_file_service)
    ):
    file = await services.upload_file(
        upload_file=file,
        user_id=current_user.user_id,
        db=db
        )
    return file