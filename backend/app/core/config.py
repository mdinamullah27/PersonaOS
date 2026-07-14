"""Application configuration using Pydantic Settings.

Centralizes all configuration management with environment variable support,
validation, and type safety.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Supports .env file loading and validates all configuration values.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "PersonaOS"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "AI Digital Twin Platform"
    DEBUG: bool = False
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: SecretStr = Field(
        default=SecretStr("change-me-in-production"),
        description="Secret key for JWT signing",
    )
    JWT_EXPIRE_MINUTES: int = Field(default=30, ge=1, description="JWT token expiry in minutes")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:1234@localhost:5433/personaos",
        description="Async PostgreSQL connection string",
    )
    DATABASE_ECHO: bool = Field(default=False, description="SQLAlchemy echo mode")
    DATABASE_POOL_SIZE: int = Field(default=20, ge=1, description="Connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, ge=0, description="Max overflow connections")

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string",
    )

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "console"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings singleton.

    Returns:
        Settings: Application configuration instance.
    """
    return Settings()
