from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_TITLE: str = "File Upload & Text Extraction Service"

    DEBUG: bool = True


settings = Config()
