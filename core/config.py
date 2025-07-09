from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL
import os


def get_env_file():
    environment = os.getenv("ENVIRONMENT", "dev")
    return f".env.{environment}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_file(), extra="ignore")

    gemini_api_key: str
    api_key: str

    db_engine: str
    db_user: str | None = None
    db_password: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None

    @computed_field
    @property
    def database_url(self) -> str:
        if self.db_engine == "sqlite":
            return f"sqlite:///./{self.db_name}"
        
        return str(URL.create(
            drivername=self.db_engine,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ))


settings = Settings()
