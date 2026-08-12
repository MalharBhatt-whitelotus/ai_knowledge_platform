from fastapi import APIRouter

from services.embedding.app.api.routes.health import router as health_router
from services.embedding.app.api.routes.embedding_routes import embedding_router
from shared_lib.observability.routes import router

api_router = APIRouter()

api_router.include_router(
        health_router, 
        tags=["Health"],
        )

api_router.include_router(
        embedding_router, 
        tags=["Embeddings"],
        )

api_router.include_router(router, tags=["metrics"])