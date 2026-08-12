from fastapi import APIRouter

from services.auth.app.api.routes.health import router as health_router
from services.auth.app.api.routes.auth_routes import router as auth_router
from shared_lib.observability.routes import router

api_router = APIRouter()

api_router.include_router(
        health_router, 
        tags=["Health"],
        )

api_router.include_router(
        auth_router, 
        tags=["Auth_Routes"],
        )


api_router.include_router(router, tags=["metrics"])