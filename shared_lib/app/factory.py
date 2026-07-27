from fastapi import FastAPI
from fastapi.routing import APIRouter

from shared_lib.config.settings import settings

def create_app(service_name: str, router: APIRouter) -> FastAPI:
    """
    Creata and configure a FastAPI Application.
    """
    app = FastAPI(title=service_name, version=settings.APP_VERSION)
    app.include_router(router)

    return app