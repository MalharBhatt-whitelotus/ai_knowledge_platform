from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

Base_Path = Path(__file__).resolve().parent.parent.parent

class OpenAISetting(BaseSettings):

    OPENAI_API_KEY: str
    OPENAI_MODEL: str

    model_config = SettingsConfigDict(env_file=Base_Path/".env", extra="ignore")

settings = OpenAISetting()