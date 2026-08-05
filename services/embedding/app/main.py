from fastapi import FastAPI

from services.embedding.app.api.router import api_router
from services.embedding.app.services import embedding_service

from shared_lib.core.factory import create_app


async def startup(app: FastAPI):
    embedding_service.load_model()

async def shutdown(app: FastAPI):
    embedding_service.model = None

app = create_app(
        service_name = "Embedding Service",
        router = api_router,
        startup=startup,
        shutdown=shutdown,
        )