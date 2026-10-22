"""Application settings. The only place that reads environment variables."""
from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"), extra="ignore", env_file_encoding="utf-8"
    )

    app_env: str = "development"
    database_url: str = "sqlite:///./saathi.db"
    timezone: str = "Asia/Kolkata"
    shared_secret: str = ""
    cors_origins: str = "http://localhost:5173"
    telegram_bot_token: str = ""
    missed_dose_minutes: int = 60
    llm_provider: Literal["rules", "gemini", "groq"] = "rules"
    gemini_api_key: str = ""
    groq_api_key: str = ""
    mcp_public_url: str = "http://localhost:8000/mcp"

    @field_validator("shared_secret", "telegram_bot_token", mode="before")
    @classmethod
    def _strip(cls, v: object) -> object:
        return v.strip() if isinstance(v, str) else v

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def auth_enabled(self) -> bool:
        return bool(self.shared_secret)


@lru_cache
def get_settings() -> Settings:
    return Settings()
