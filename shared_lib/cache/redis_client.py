import redis.asyncio as redis

from shared_lib.config.settings import settings


class RedisClient:


    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )


    async def get(self, key: str):
        return await self.client.get(key)


    async def set(
            self,
            key: str,
            value: str,
            ttl: int,
    ):
        await self.client.set(key, value, ex=ttl)

    async def delete(self, key: str):
        await self.client.delete(key)

    async def close(self):
        await self.client.aclose()