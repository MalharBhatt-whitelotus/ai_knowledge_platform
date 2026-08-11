from fastapi import FastAPI

from shared_lib.core.factory import create_app
from shared_lib.core.rate_limiter import RateLimiter
from shared_lib.cache.redis_client import RedisClient

from services.worker.app.config.worker_config import settings
from services.worker.app.messaging.rabbitmq import RabbitMQConnection 
from services.worker.app.messaging.publisher import RabbitMQPublisher

from services.file.app.api.router import api_router


redis_client = RedisClient()

rate_limiter = RateLimiter(
    redis=redis_client,
    max_requests=20,
    window_seconds=60,
)

async def startup(app: FastAPI):
    rabbitmq = RabbitMQConnection(settings.RABBITMQ_URL)
    await rabbitmq.connect()
    exchange = await rabbitmq.declare_exchange("files")

    app.state.rabbitmq = rabbitmq
    app.state.publisher = RabbitMQPublisher(exchange)

    app.state.redis = redis_client
    app.state.rate_limiter = rate_limiter


async def shutdown(app: FastAPI):
    await app.state.rabbitmq.close()
    await redis_client.close()


app = create_app(
        service_name = "File Service",
        router = api_router,
        startup=startup,
        shutdown=shutdown,
        rate_limiter=rate_limiter,
        )       