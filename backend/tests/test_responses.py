"""Tests for API response models.

Tests the unified response models for consistency.
"""

import pytest

from app.core.responses import (
    ErrorResponse,
    PaginatedData,
    PaginatedResponse,
    ResponseMeta,
    SuccessResponse,
    error_response,
    success_response,
)


@pytest.mark.unit
class TestResponseModels:
    """Test response model schemas."""

    def test_success_response_structure(self) -> None:
        """Test SuccessResponse has correct structure."""
        response = SuccessResponse(data={"key": "value"}, message="Success")

        assert response.success is True
        assert response.data == {"key": "value"}
        assert response.message == "Success"

    def test_error_response_structure(self) -> None:
        """Test ErrorResponse has correct structure."""
        response = ErrorResponse(
            message="Error occurred",
            code="TEST_ERROR",
            details={"reason": "testing"},
        )

        assert response.success is False
        assert response.message == "Error occurred"
        assert response.code == "TEST_ERROR"
        assert response.details == {"reason": "testing"}

    def test_paginated_data_structure(self) -> None:
        """Test PaginatedData has correct structure."""
        data = PaginatedData(
            items=[1, 2, 3],
            total=10,
            page=1,
            page_size=3,
            pages=4,
        )

        assert data.items == [1, 2, 3]
        assert data.total == 10
        assert data.page == 1
        assert data.page_size == 3
        assert data.pages == 4

    def test_paginated_response_structure(self) -> None:
        """Test PaginatedResponse has correct structure."""
        paginated_data = PaginatedData(
            items=["a", "b"],
            total=5,
            page=1,
            page_size=2,
            pages=3,
        )
        response = PaginatedResponse(data=paginated_data)

        assert response.success is True
        assert response.data.items == ["a", "b"]
        assert response.data.total == 5

    def test_response_meta_defaults(self) -> None:
        """Test ResponseMeta has correct defaults."""
        meta = ResponseMeta()

        assert meta.version == "v1"
        assert meta.request_id is None
        assert meta.timestamp is None


@pytest.mark.unit
class TestResponseHelpers:
    """Test response helper functions."""

    def test_success_response_function(self) -> None:
        """Test success_response helper returns dict."""
        result = success_response(data={"id": 1}, message="Created")

        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["data"] == {"id": 1}
        assert result["message"] == "Created"

    def test_error_response_function(self) -> None:
        """Test error_response helper returns dict."""
        result = error_response(
            message="Failed",
            code="FAIL",
            details={"error": "details"},
        )

        assert isinstance(result, dict)
        assert result["success"] is False
        assert result["message"] == "Failed"
        assert result["code"] == "FAIL"

    def test_success_response_none_data(self) -> None:
        """Test success_response with None data."""
        result = success_response(data=None)

        assert result["success"] is True
        assert result["data"] is None

    def test_error_response_defaults(self) -> None:
        """Test error_response with defaults."""
        result = error_response()

        assert result["success"] is False
        assert result["code"] == "ERROR"
