"""User schemas.

Pydantic models for user requests and responses.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field

from app.core.constants import UserRole


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., description="Username")
    full_name: str | None = Field(None, description="Full name")


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=128, description="Password")
    role: UserRole = Field(default=UserRole.MEMBER, description="User role")


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    full_name: str | None = Field(None, description="Full name")
    username: str | None = Field(None, description="Username")


class UserResponse(UserBase):
    """Schema for user responses."""

    id: str = Field(..., description="User ID")
    role: UserRole = Field(..., description="User role")
    is_active: bool = Field(..., description="Account active status")
    is_verified: bool = Field(..., description="Email verified status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Schema for user list responses."""

    items: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total pages")
