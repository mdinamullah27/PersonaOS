"""Tests for core configuration.

Tests Pydantic Settings configuration and validation.
"""

import pytest

from app.core.config import get_settings


@pytest.mark.unit
class TestSettings:
    """Test configuration settings."""

    def test_get_settings_singleton(self) -> None:
        """Test that get_settings returns a singleton."""
        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_settings_has_defaults(self) -> None:
        """Test that settings have default values."""
        settings = get_settings()

        assert settings.APP_NAME == "PersonaOS"
        assert settings.APP_VERSION == "0.1.0"
        assert settings.API_V1_PREFIX == "/api/v1"
        assert settings.JWT_ALGORITHM == "HS256"

    def test_settings_database_url(self) -> None:
        """Test database URL setting exists."""
        settings = get_settings()

        assert settings.DATABASE_URL is not None
        assert "postgresql" in settings.DATABASE_URL or "sqlite" in settings.DATABASE_URL

    def test_settings_redis_url(self) -> None:
        """Test Redis URL setting exists."""
        settings = get_settings()

        assert settings.REDIS_URL is not None
        assert "redis" in settings.REDIS_URL

    def test_settings_environment_helpers(self) -> None:
        """Test environment helper properties."""
        settings = get_settings()

        assert settings.is_development is not None
        assert settings.is_production is not None
        assert isinstance(settings.is_development, bool)
        assert isinstance(settings.is_production, bool)
