"""Authentication exceptions.

Custom exceptions for authentication and authorization errors.
"""

from app.core.exceptions import BaseAppException


class AuthenticationError(BaseAppException):
    """Raised when authentication fails."""

    status_code = 401
    code = "AUTHENTICATION_ERROR"
    message = "Invalid credentials"


class InvalidTokenError(BaseAppException):
    """Raised when JWT token is invalid or expired."""

    status_code = 401
    code = "INVALID_TOKEN"
    message = "Invalid or expired token"


class InsufficientPermissionsError(BaseAppException):
    """Raised when user lacks required permissions."""

    status_code = 403
    code = "INSUFFICIENT_PERMISSIONS"
    message = "You do not have permission to perform this action"
