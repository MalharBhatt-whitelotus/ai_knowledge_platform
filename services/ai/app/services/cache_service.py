from shared_lib.config.settings import settings
from shared_lib.cache.redis_client import RedisClient


class CacheService:


    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client


    async def get(self, key: str):
        return await self.redis.get(key=key)


    async def set(self, key: str, value: str):
        await self.redis.set(key=key, value=value, ttl=settings.REDIS_CACHE_TTL,)


    async def delete(self, key: str):
        await self.redis.delete(key=key)