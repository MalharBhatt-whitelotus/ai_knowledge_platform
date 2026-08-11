import time
from redis.asyncio import Redis
from fastapi.requests import Request


class RateLimiter:


    def __init__(
            self,
            redis: Redis,
            max_requests: int = 100,
            window_seconds: int = 60,
            ):
        self.redis =redis
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, request: Request) -> bool:
        client_ip = request.client.host

        window = int(time.time() // self.window_seconds)

        key = f"rate_limit:{client_ip}:{window}"

        count = await self.redis.increment(key)

        if count == 1:
            await self.redis.expire(key, self.window_seconds,)

        return count <= self.max_requests