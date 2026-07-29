from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AuthSettings(BaseSettings):

    SERVICE_NAME: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int =7
    JWT_ALGORITHMS: str = "HS256"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=BASE_DIR/".env", extra="ignore")

@lru_cache
def get_settings() -> AuthSettings:
    return AuthSettings()

settings =  get_settings()
print("BASE_DIR =", BASE_DIR)
print("ENV FILE =", BASE_DIR / ".env")
print("DATABASE_URL =", settings.DATABASE_URL)