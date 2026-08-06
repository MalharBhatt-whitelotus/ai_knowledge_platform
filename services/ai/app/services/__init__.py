from services.ai.app.services.ai_service import AIService
from services.ai.app.clients.genai_client import GenaiClient
from services.ai.app.clients.search_client import SearchClient
from services.ai.app.services.prompt_builder import PromptBuilder


service = AIService(
    search_client=SearchClient(), 
    prompt_builder=PromptBuilder(), 
    genai_client=GenaiClient()
    )