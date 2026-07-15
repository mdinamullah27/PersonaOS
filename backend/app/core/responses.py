"""Unified API response models for consistent API responses.

Provides standardized response formats for success, error, and paginated responses.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMeta(BaseModel):
    """Response metadata model."""

    request_id: str | None = Field(default=None, description="Request correlation ID")
    timestamp: str | None = Field(default=None, description="Response timestamp")
    version: str = Field(default="v1", description="API version")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response model.

    Attributes:
        success: Always True for successful responses.
        data: Response data payload.
        message: Optional success message.
    """

    success: bool = True
    data: T | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    """Standard error response model.

    Attributes:
        success: Always False for error responses.
        message: Human-readable error message.
        code: Application-specific error code.
        details: Additional error details.
        meta: Response metadata.
    """

    success: bool = False
    message: str = "An error occurred"
    code: str = "ERROR"
    details: dict[str, Any] | None = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class PaginatedData(BaseModel, Generic[T]):
    """Paginated data wrapper.

    Attributes:
        items: List of items.
        total: Total number of items.
        page: Current page number.
        page_size: Items per page.
        pages: Total number of pages.
    """

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model.

    Attributes:
        success: Always True for successful responses.
        data: Paginated data.
        meta: Response metadata.
    """

    success: bool = True
    data: PaginatedData[T]
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


def success_response(
    data: Any = None,
    message: str | None = None,
) -> dict[str, Any]:
    """Create a success response dictionary.

    Args:
        data: Response data.
        message: Optional success message.

    Returns:
        Formatted success response dictionary.
    """
    return SuccessResponse(
        data=data,
        message=message,
    ).model_dump()


def error_response(
    message: str = "An error occurred",
    code: str = "ERROR",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an error response dictionary.

    Args:
        message: Error message.
        code: Error code.
        details: Additional error details.

    Returns:
        Formatted error response dictionary.
    """
    return ErrorResponse(
        message=message,
        code=code,
        details=details,
    ).model_dump()
