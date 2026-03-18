from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경 변수 기반 설정 객체."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="HermesForge", alias="HERMES_APP_NAME")
    env: str = Field(default="development", alias="HERMES_ENV")
    log_level: str = Field(default="INFO", alias="HERMES_LOG_LEVEL")
    db_path: str = Field(default="backend/hermesforge.db", alias="HERMES_DB_PATH")
    api_prefix: str = Field(default="/api", alias="HERMES_API_PREFIX")
    allowed_origins: str = Field(default="http://localhost:5173", alias="HERMES_ALLOWED_ORIGINS")

    @property
    def allowed_origins_list(self) -> List[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
