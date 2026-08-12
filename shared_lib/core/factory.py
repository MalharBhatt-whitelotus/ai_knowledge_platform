from contextlib import asynccontextmanager
from collections.abc import Callable, Awaitable

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from shared_lib.logger.logger import get_logger
from shared_lib.config.settings import settings
from shared_lib.exceptions.exceptions import AppException
from shared_lib.core.middleware import register_middleware
from shared_lib.core.exception_handler import app_exception_handler
from shared_lib.core.rate_limiter import RateLimiter
from shared_lib.observability.routes import router as metrics_router
from shared_lib.observability.health import router as health_router

StartupCallback = Callable[[FastAPI], Awaitable[None]]
ShutdownCallback = Callable[[FastAPI], Awaitable[None]]


def create_app(
        service_name: str, 
        router: APIRouter,
        startup: StartupCallback | None = None,
        shutdown: ShutdownCallback | None = None,
        rate_limiter: RateLimiter = None,
        ) -> FastAPI:
    """
    Creata and configure a FastAPI Application.
    """

    logger = get_logger(service_name)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info(f"{service_name} starting...")

        if startup:
            await startup(app)
        yield
        if shutdown:
            await shutdown(app)

        logger.info(f"{service_name} shutting down...")

    app = FastAPI(
        title=service_name, 
        version=settings.APP_VERSION, 
        lifespan=lifespan
        )

    register_middleware(app, logger, service_name=service_name, rate_limiter=rate_limiter)
    app.add_exception_handler(AppException, app_exception_handler,)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    app.include_router(health_router, tags=["Health"])
    app.include_router(metrics_router, tags=["Metrics"])

    return app