from fastapi import APIRouter

from services.search.app.api.routes.health import router as health_router
from services.search.app.api.routes.search_routes import search_router
from shared_lib.observability.routes import router

api_router = APIRouter()

api_router.include_router(
        health_router, 
        tags=["Health"],
        )

api_router.include_router(
        search_router, 
        tags=["Search"],
        )


api_router.include_router(router, tags=["metrics"])