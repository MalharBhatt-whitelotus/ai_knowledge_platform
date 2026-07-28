from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AuthSettings(BaseSettings):

    SERVICE_NAME: str

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR/".env", extra="ignore")

@lru_cache
def get_settings() -> AuthSettings:
    return AuthSettings()

settings =  get_settings()