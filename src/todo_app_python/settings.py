from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DSN: str = Field("postgresql+asyncpg://todoapp:todoapp1234@127.0.0.1:5432/todoapp")

    model_config = SettingsConfigDict(env_prefix="app_")


settings = Settings()
