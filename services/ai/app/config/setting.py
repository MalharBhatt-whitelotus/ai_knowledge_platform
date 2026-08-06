from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

Base_Path = Path(__file__).resolve().parent.parent.parent

class GenAISetting(BaseSettings):

    GENAI_API_KEY: str
    GENAI_MODEL: str

    model_config = SettingsConfigDict(env_file=Base_Path/".env", extra="ignore")

settings = GenAISetting()