from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,status,UploadFile,File, Depends
from fastapi.responses import StreamingResponse, PlainTextResponse

from services.file.app.database.file_database import get_db
from services.file.app.dependencies.file_dependency import get_file_service
from services.file.app.services.file_services import FileServices
from services.file.app.schemas.file_schemas import FileResponse, FileUploadResponse

from shared_lib.dependencies.role_checker import user_only


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


@file_router.get("/get_file/{file_id}", response_model=FileResponse, status_code=status.HTTP_200_OK)
async def get_file(
    file_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(user_only),
    services: FileServices = Depends(get_file_service)):

    file = await services.get_file_by_file_id(file_id, current_user.user_id, db)

    return file


@file_router.get("/internal/get_file/{file_id}", response_model=FileResponse, status_code=status.HTTP_200_OK)
async def get_file(
    file_id: str,  
    db: AsyncSession = Depends(get_db), 
    services: FileServices = Depends(get_file_service)
    ):

    file = await services.get_internal_file(file_id, db)
    
    return file


@file_router.get("/internal/download_file/{file_id}", response_class=StreamingResponse, status_code=status.HTTP_200_OK)
async def download_file(
    file_id: str,
    db: AsyncSession = Depends(get_db),
    services: FileServices = Depends(get_file_service),
):
    
    file_bytes = await services.get_file_bytes(file_id, db)

    return StreamingResponse(content= BytesIO(file_bytes))

@file_router.get("/internal/extract_text/{file_id}", response_class=PlainTextResponse, status_code=status.HTTP_200_OK)
async def extract_text(
    file_id: str, 
    db: AsyncSession = Depends(get_db), 
    services: FileServices = Depends(get_file_service)
    ):

    text = await services.extract_text(file_id, db)

    return text