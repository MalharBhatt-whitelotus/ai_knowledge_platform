from fastapi import APIRouter

from services.file.app.api.routes.health import router as health_router
from services.file.app.api.routes.file_routes import file_router

api_router = APIRouter()

api_router.include_router(
        health_router, 
        tags=["Health"],
        )

api_router.include_router(
    file_router,
    tags=["files"]
    )