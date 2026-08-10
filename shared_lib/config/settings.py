from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "AI Knowledge Platform"
    APP_VERSION: str = "1.0.0"

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASSWORD: str

    OPEN_AI_KEY: str

    RETRY_ATTEMPTS: int = 3
    RETRY_MIN_WAIT: int = 1
    RETRY_MAX_WAIT: int = 8

    AUTH_URL: str
    FILE_URL: str
    EMBEDDING_URL: str
    SEARCH_URL: str

    model_config = SettingsConfigDict(env_file=  ".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()