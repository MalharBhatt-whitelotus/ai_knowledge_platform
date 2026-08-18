from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    auth_service_url : str = "http://auth_service:8001"
    file_service_url : str = "http://file_service:8002"
    ai_service_url : str = "http://ai_service:8005"

    model_config = SettingsConfigDict(env_file= ".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()