from fastapi import FastAPI

from shared_lib.config.settings import settings
from gateway_service.app.api.router import api_router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(api_router)