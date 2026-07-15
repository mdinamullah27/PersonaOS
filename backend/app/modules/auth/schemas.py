"""Authentication schemas.

Pydantic models for authentication requests and responses.
"""

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiry in seconds")
