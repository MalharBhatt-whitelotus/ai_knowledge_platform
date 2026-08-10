from shared_lib.clients.search_client import SearchClient
from shared_lib.cache.redis_client import RedisClient

from services.ai.app.services.ai_service import AIService
from services.ai.app.clients.genai_client import GenaiClient
from services.ai.app.services.prompt_builder import PromptBuilder
from services.ai.app.services.cache_service import CacheService

redis_client = RedisClient()

service = AIService(
    search_client=SearchClient(), 
    prompt_builder=PromptBuilder(), 
    genai_client=GenaiClient(),
    cache_service=CacheService(redis_client=redis_client),
    )