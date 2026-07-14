"""Test configuration and fixtures.

Provides shared fixtures for all tests.
"""

from collections.abc import AsyncGenerator
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings
from main import app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Backend for anyio tests.

    Returns:
        Backend name.
    """
    return "asyncio"


@pytest.fixture
def settings() -> Any:
    """Get application settings.

    Returns:
        Settings instance.
    """
    return get_settings()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client.

    Yields:
        AsyncClient for testing.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_user_data() -> dict[str, Any]:
    """Sample user data for testing.

    Returns:
        User data dictionary.
    """
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123",
        "full_name": "Test User",
    }


@pytest.fixture
def mock_login_data() -> dict[str, str]:
    """Sample login credentials for testing.

    Returns:
        Login data dictionary.
    """
    return {
        "email": "test@example.com",
        "password": "securepassword123",
    }
