from fastapi import APIRouter

from services.embedding.app.api.routes.embedding_routes import embedding_router

api_router = APIRouter()

api_router.include_router(
        embedding_router, 
        tags=["Embeddings"],
        )