import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class Config(BaseSettings):
    APP_TITLE: str = "Text Extractor Service"
    POSTGRES_URL: PostgresDsn
    CORS_ORIGINS: str

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8")


settings = Config()
