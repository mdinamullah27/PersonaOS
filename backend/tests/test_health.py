"""Tests for health check endpoints.

Tests the health, readiness, and version endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.unit
class TestHealthEndpoints:
    """Test health check endpoints."""

    async def test_health_check(self, client: AsyncClient) -> None:
        """Test health endpoint returns healthy status."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        assert "timestamp" in data["data"]

    async def test_version_info(self, client: AsyncClient) -> None:
        """Test version endpoint returns version information."""
        response = await client.get("/version")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "version" in data["data"]
        assert "environment" in data["data"]

    async def test_readiness_check(self, client: AsyncClient) -> None:
        """Test readiness endpoint returns dependency status."""
        response = await client.get("/ready")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "checks" in data["data"]
