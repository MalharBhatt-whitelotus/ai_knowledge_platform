from fastapi import APIRouter

from shared_lib.observability.routes import router
from services.ai.app.api.routes.ai_routes import ai_router
from services.ai.app.api.routes.health import router as health_router

api_router = APIRouter()

api_router.include_router(
        health_router, 
        tags=["Health"],
        )

api_router.include_router(
        ai_router, 
        tags=["AI"],
        )


api_router.include_router(router, tags=["metrics"])