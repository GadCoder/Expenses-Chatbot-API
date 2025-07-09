import os
from typing import Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file():
    environment = os.getenv("ENVIRONMENT", "dev")
    return f".env.{environment}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_file(), extra="ignore")

    gemini_api_key: str
    api_key: str

    DB_ENGINE: str
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = None

    @computed_field
    @property
    def database_url(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return f"sqlite:///./{self.DB_NAME}"
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
