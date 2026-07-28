from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AuthSettings(BaseSettings):

    SERVICE_NAME: str

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int =7
    JWT_ALGORITHMS: str = "HS256"


    model_config = SettingsConfigDict(env_file=BASE_DIR/".env", extra="ignore")

@lru_cache
def get_settings() -> AuthSettings:
    return AuthSettings()

settings =  get_settings()