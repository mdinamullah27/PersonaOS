"""Common dependency injection providers.

Provides reusable dependencies for FastAPI route injection.
"""

from typing import Annotated

from fastapi import Depends, Header, Query, Request
from pydantic import BaseModel, Field

from app.core.constants import PaginationDefaults


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate database offset."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Calculate database limit."""
        return self.page_size


async def get_pagination(
    page: int = Query(
        default=int(PaginationDefaults.PAGE.value),
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=int(PaginationDefaults.PAGE_SIZE.value),
        ge=1,
        le=int(PaginationDefaults.MAX_PAGE_SIZE.value),
        description="Items per page",
    ),
) -> PaginationParams:
    """Dependency for pagination parameters.

    Args:
        page: Page number.
        page_size: Items per page.

    Returns:
        PaginationParams instance.
    """
    return PaginationParams(page=page, page_size=page_size)


async def get_request_id(
    request: Request,
    x_request_id: str | None = Header(default=None, alias="X-Request-ID"),
) -> str | None:
    """Extract or generate request ID for tracing.

    Args:
        request: FastAPI request object.
        x_request_id: Optional request ID from header.

    Returns:
        Request ID string.
    """
    request_id = x_request_id or getattr(request.state, "request_id", None)
    return request_id


class CommonQueryParams(BaseModel):
    """Common query parameters for filtering and sorting."""

    q: str | None = Field(default=None, description="Search query")
    sort_by: str | None = Field(default=None, description="Sort field")
    sort_order: str = Field(default="desc", description="Sort order (asc/desc)")


async def get_common_query(
    q: str | None = Query(default=None, description="Search query"),
    sort_by: str | None = Query(default=None, description="Sort field"),
    sort_order: str = Query(default="desc", description="Sort order"),
) -> CommonQueryParams:
    """Dependency for common query parameters.

    Args:
        q: Search query string.
        sort_by: Field to sort by.
        sort_order: Sort direction.

    Returns:
        CommonQueryParams instance.
    """
    return CommonQueryParams(q=q, sort_by=sort_by, sort_order=sort_order)
