from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- App ---
    APP_NAME: str = "TalentFlow AI"
    APP_ENV: Literal["development", "test", "production"] = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # --- Security ---
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h; see ADR-004

    # --- Database ---
    DATABASE_URL: str = Field(...)

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173"

    # --- AI Provider (see ADR-006) ---
    AI_PROVIDER: Literal["mock", "openai_compatible"] = "mock"
    AI_API_KEY: str | None = None
    AI_BASE_URL: str = "https://api.openai.com/v1"
    AI_MODEL: str = "gpt-4o-mini"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        # SQLAlchemy 2.x + psycopg require "postgresql+psycopg://", but
        # Supabase/Render commonly hand out "postgres://" or "postgresql://".
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+psycopg://", 1)
        elif v.startswith("postgresql://") and "+psycopg" not in v:
            v = v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
