from fastapi import FastAPI

from shared_lib.core.factory import create_app
from shared_lib.logger.logger import get_logger
from services.worker.app.api.router import api_router
from services.worker.app.config.worker_config import settings
from services.worker.app.messaging.rabbitmq import RabbitMQConnection
from services.worker.app.handlers.file_uploaded_handlers import FileUploadedHandler
from services.worker.app.consumers.file_uploaded_consumer import FileUploadedConsumer

from services.worker.app.clients.file_client import FileClient
from services.worker.app.clients.search_client import SearchClient
from services.worker.app.clients.embedding_client import EmbeddingClient

logger = get_logger(__name__)

async def startup(app: FastAPI):
    logger.info(">>> RabbitMQ URL: %s", settings.RABBITMQ_URL)

    rabbitmq = RabbitMQConnection(settings.RABBITMQ_URL)

    await rabbitmq.connect()

    exchange = await rabbitmq.declare_exchange("files")

    queue = await rabbitmq.declare_queue(
        queue_name="file-processing",
        routing_key="file.uploaded",
    )
    
    handler = FileUploadedHandler(FileClient, EmbeddingClient, SearchClient)
    consumer = FileUploadedConsumer(rabbitmq,handler)

    await queue.consume(consumer.consume)

    app.state.rabbitmq = rabbitmq
    app.state.consumer = consumer

async def shutdown(app: FastAPI):
    await app.state.rabbitmq.close()


app = create_app(
        service_name = "Worker Service",
        router = api_router,
        startup=startup,
        shutdown=shutdown
        )