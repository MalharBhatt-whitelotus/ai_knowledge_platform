from fastapi import APIRouter

from services.auth.app.api.routes.health import router as health_router
from services.auth.app.api.routes.register_route import register_router

api_router = APIRouter()

api_router.include_router(
        health_router, 
        tags=["Health"],
        )

api_router.include_router(
        register_router, 
        tags=["Register"],
        )