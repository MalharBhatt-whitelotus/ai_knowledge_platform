from fastapi import FastAPI

from shared_lib.core.factory import create_app
from shared_lib.core.rate_limiter import RateLimiter
from shared_lib.cache.redis_client import RedisClient

from services.auth.app.api.router import api_router


redis_client = RedisClient()

rate_limiter = RateLimiter(
    redis=redis_client,
    max_requests=20,
    window_seconds=60,
)


async def startup(app: FastAPI):
    app.state.redis = redis_client
    app.state.rate_limiter = rate_limiter


async def shutdown(app: FastAPI):

    await redis_client.close()


app = create_app(
        service_name = "Auth Service",
        router = api_router,
        startup=startup,
        shutdown=shutdown,
        rate_limiter=rate_limiter,
        )