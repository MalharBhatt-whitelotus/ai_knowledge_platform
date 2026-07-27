from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRouter

from shared_lib.config.settings import settings
from shared_lib.logger.logger import get_logger
from shared_lib.exceptions.exceptions import AppException
from shared_lib.app.exception_handler import app_exception_handler

def create_app(service_name: str, router: APIRouter) -> FastAPI:
    """
    Creata and configure a FastAPI Application.
    """

    logger = get_logger(service_name)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info(f"{service_name} starting...")
        yield
        logger.info(f"{service_name} shutting down...")

    app = FastAPI(
        title=service_name, 
        version=settings.APP_VERSION, 
        lifespan=lifespan
        )

    app.add_exception_handler(AppException, app_exception_handler,)
    
    app.include_router(router)

    return app