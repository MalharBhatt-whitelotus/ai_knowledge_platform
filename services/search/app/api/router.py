from fastapi import APIRouter

from services.search.app.api.routes.search_routes import search_router

api_router = APIRouter()

api_router.include_router(
        search_router, 
        tags=["Search"],
        )