from fastapi import FastAPI

from shared_lib.core.factory import create_app
from shared_lib.logger.logger import get_logger
from shared_lib.clients.file_client import FileClient
from shared_lib.clients.search_client import SearchClient
from shared_lib.clients.embedding_client import EmbeddingClient

from services.worker.app.api.router import api_router
from services.worker.app.config.worker_config import settings
from services.worker.app.messaging.rabbitmq import RabbitMQConnection
from services.worker.app.handlers.file_uploaded_handlers import FileUploadedHandler
from services.worker.app.consumers.file_uploaded_consumer import FileUploadedConsumer
from services.worker.app.messaging.rabbitmq_topology import RabbitmqTopology
from services.worker.app.messaging.retry_publisher import RetryPublisher


logger = get_logger(__name__)


async def startup(app: FastAPI):
    logger.info(">>> RabbitMQ URL: %s", settings.RABBITMQ_URL)

    rabbitmq = RabbitMQConnection(settings.RABBITMQ_URL)

    await rabbitmq.connect()

    topology = RabbitmqTopology()
    resources = await topology.setup(rabbitmq=rabbitmq,)

    retry_publisher = RetryPublisher(
        retry_exchange=resources["retry_exchange"], 
        dlq_exchange=resources["dlq_exchange"],
        )

    handler = FileUploadedHandler(FileClient, EmbeddingClient, SearchClient)
    consumer = FileUploadedConsumer(handler=handler, retry_publisher=retry_publisher,)


    logger.info(
        "MAIN QUEUE = %s",
        resources["main_queue"].name,
    )

    logger.info(
        "REGISTERING FILE UPLOADED CONSUMER..."
        )

    await resources["main_queue"].consume(consumer.consume)
    logger.info(
        "FILE UPLOADED CONSUMER REGISTERED"
        )
    

    app.state.rabbitmq = rabbitmq
    app.state.consumer = consumer

    logger.info("Worker_service started successfully.")


async def shutdown(app: FastAPI):
    logger.info("Shutting down Worker Service...")
    if hasattr(app.state, "rabbitmq"):
        await app.state.rabbitmq.close()
    logger.info("Worker Service is shutdown completely.")


app = create_app(
        service_name = "Worker Service",
        router = api_router,
        startup=startup,
        shutdown=shutdown
        )