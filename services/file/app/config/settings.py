from pathlib import Path
from functools import lru_cache
from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class FileSettings(BaseSettings):

    SERVICE_NAME: str

    POSTGRES_HOST: str
    SHARED_POSTGRES_PORT: str
    FILE_POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.SHARED_POSTGRES_PORT}"
            f"/{self.FILE_POSTGRES_DB}"
            )

    model_config = SettingsConfigDict(env_file=BASE_DIR/".env", extra="ignore")

@lru_cache
def get_settings() -> FileSettings:
    return FileSettings()

settings = get_settings()
print("BASE_DIR =", BASE_DIR)
print("ENV FILE =", BASE_DIR / ".env")
print("DATABASE_URL =", settings.DATABASE_URL)