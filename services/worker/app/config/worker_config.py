from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class WorkerSetting(BaseSettings):

    RABBITMQ_HOST: str
    SHARED_RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def RABBITMQ_URL(self):
        return (
            f"amqp://"
            f"{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.SHARED_RABBITMQ_PORT}/"
        )

settings = WorkerSetting()
# print("BASE_DIR =", BASE_DIR)
print("ENV FILE =",  ".env")
print("RABBITMQ_URL =", settings.RABBITMQ_URL)