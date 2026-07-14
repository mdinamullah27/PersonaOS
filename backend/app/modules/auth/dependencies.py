"""Authentication dependencies for FastAPI.

Provides dependencies for authentication and authorization.
"""

from typing import Annotated

from fastapi import Depends, Header
from pydantic import BaseModel

from app.core.constants import Permission, UserRole
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token
from app.modules.auth.exceptions import (
    InsufficientPermissionsError,
    InvalidTokenError,
)
from app.modules.auth.constants import AUTH_HEADER_NAME, AUTH_HEADER_PREFIX


class CurrentUser(BaseModel):
    """Current authenticated user model.

    Represents the authenticated user context.
    """

    id: str
    email: str
    username: str
    role: UserRole
    is_active: bool = True

    class Config:
        """Pydantic config."""

        use_enum_values = True


async def get_current_user(
    authorization: str | None = Header(default=None, alias=AUTH_HEADER_NAME),
) -> CurrentUser:
    """Extract and validate current user from JWT token.

    Args:
        authorization: Authorization header value.

    Returns:
        CurrentUser: Authenticated user context.

    Raises:
        InvalidTokenError: If token is invalid or missing.
    """
    if not authorization:
        raise InvalidTokenError(message="Authorization header is required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != AUTH_HEADER_PREFIX.lower():
        raise InvalidTokenError(message="Invalid authorization header format")

    token = parts[1]

    try:
        payload = decode_token(token)
    except Exception as exc:
        raise InvalidTokenError(message=f"Invalid token: {exc}") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError(message="Invalid token payload")

    # In Phase 2, fetch user from database
    # For now, return a mock user context
    return CurrentUser(
        id=user_id,
        email=payload.get("email", ""),
        username=payload.get("username", ""),
        role=payload.get("role", UserRole.MEMBER),
        is_active=payload.get("is_active", True),
    )


# Type annotation for current user dependency
CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


def require_permissions(*required_permissions: Permission):
    """Dependency factory for permission-based authorization.

    Args:
        *required_permissions: Required permissions.

    Returns:
        Dependency function that checks permissions.

    Example:
        @router.get("/admin")
        async def admin_endpoint(
            current_user: CurrentUserDep,
            _: None = Depends(require_permissions(Permission.ADMIN_PANEL)),
        ):
            return {"message": "Admin access granted"}
    """

    async def check_permissions(
        current_user: CurrentUserDep,
    ) -> CurrentUser:
        """Check if current user has required permissions.

        Args:
            current_user: Authenticated user.

        Returns:
            CurrentUser if authorized.

        Raises:
            InsufficientPermissionsError: If user lacks permissions.
        """
        from app.core.constants import ROLE_PERMISSIONS

        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])

        for permission in required_permissions:
            if permission not in user_permissions:
                raise InsufficientPermissionsError(
                    message=f"Missing permission: {permission.value}",
                    details={
                        "required": [p.value for p in required_permissions],
                        "current": [p.value for p in user_permissions],
                    },
                )

        return current_user

    return check_permissions


def require_role(*allowed_roles: UserRole):
    """Dependency factory for role-based authorization.

    Args:
        *allowed_roles: Allowed user roles.

    Returns:
        Dependency function that checks roles.
    """

    async def check_role(
        current_user: CurrentUserDep,
    ) -> CurrentUser:
        """Check if current user has an allowed role.

        Args:
            current_user: Authenticated user.

        Returns:
            CurrentUser if authorized.

        Raises:
            InsufficientPermissionsError: If user role is not allowed.
        """
        if current_user.role not in allowed_roles:
            raise InsufficientPermissionsError(
                message=f"Role not allowed: {current_user.role}",
                details={
                    "required_roles": [r.value for r in allowed_roles],
                    "current_role": current_user.role,
                },
            )

        return current_user

    return check_role


# Common role dependencies
RequireAdmin = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN))
RequireManager = Depends(require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.MANAGER))
