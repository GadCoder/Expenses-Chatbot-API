import os
from typing import Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file():
    environment = os.getenv("ENVIRONMENT", "dev")
    return f".env.{environment}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_file(), extra="ignore")

    api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    DB_ENGINE: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = None

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"

    @computed_field
    @property
    def database_url(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return f"sqlite:///./{self.DB_NAME}.db"
        
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
