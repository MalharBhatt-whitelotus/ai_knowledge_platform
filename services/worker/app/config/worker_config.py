from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSetting(BaseSettings):

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def RABBITMQ_URL(self):
        return (
            f"amqp://"
            f"{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )

settings = WorkerSetting()
