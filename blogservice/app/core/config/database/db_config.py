import os

from pydantic import Extra, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigDataBase(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_ECHO: bool

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../.env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def get_db_url(self) -> PostgresDsn | None:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@" f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings_db = ConfigDataBase()
