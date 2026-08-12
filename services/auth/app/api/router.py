from fastapi import APIRouter

from services.auth.app.api.routes.auth_routes import router as auth_router

api_router = APIRouter()

api_router.include_router(
        auth_router, 
        tags=["Auth_Routes"],
        )