from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from shared_lib.config.settings import settings
from shared_lib.logger.logger import get_logger
from shared_lib.exceptions.exceptions import AppException
from shared_lib.core.exception_handler import app_exception_handler
from shared_lib.core.middleware import register_middleware

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
    register_middleware(app, logger)
    app.add_exception_handler(AppException, app_exception_handler,)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app