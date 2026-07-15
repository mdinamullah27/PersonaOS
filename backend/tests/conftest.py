"""Test configuration and fixtures.

Provides shared fixtures for all tests.
"""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Backend for anyio tests."""
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
