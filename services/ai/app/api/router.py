from fastapi import APIRouter

from services.ai.app.api.routes.ai_routes import ai_router

api_router = APIRouter()

api_router.include_router(
        ai_router, 
        tags=["AI"],
        )