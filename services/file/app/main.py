from fastapi import FastAPI

from services.file.app.api.router import api_router

from shared_lib.core.factory import create_app

from services.worker.app.config.worker_config import settings
from services.worker.app.messaging.rabbitmq import RabbitMQConnection 
from services.worker.app.messaging.publisher import RabbitMQPublisher


async def startup(app: FastAPI):
    rabbitmq = RabbitMQConnection(settings.RABBITMQ_URL)
    await rabbitmq.connect()
    exchange = await rabbitmq.declare_exchange("files")

    app.state.rabbitmq = rabbitmq
    app.state.publisher = RabbitMQPublisher(exchange)


async def shutdown(app: FastAPI):
      await app.state.rabbitmq.close()


app = create_app(
        service_name = "File Service",
        router = api_router,
        startup=startup,
        shutdown=shutdown,
        )       