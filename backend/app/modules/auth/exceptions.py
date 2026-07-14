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


class TokenExpiredError(BaseAppException):
    """Raised when JWT token has expired."""

    status_code = 401
    code = "TOKEN_EXPIRED"
    message = "Token has expired"


class InsufficientPermissionsError(BaseAppException):
    """Raised when user lacks required permissions."""

    status_code = 403
    code = "INSUFFICIENT_PERMISSIONS"
    message = "You do not have permission to perform this action"


class AccountDisabledError(BaseAppException):
    """Raised when user account is disabled."""

    status_code = 403
    code = "ACCOUNT_DISABLED"
    message = "Account is disabled"


class AccountLockedError(BaseAppException):
    """Raised when user account is locked due to too many failed attempts."""

    status_code = 423
    code = "ACCOUNT_LOCKED"
    message = "Account is temporarily locked"


class EmailAlreadyExistsError(BaseAppException):
    """Raised when trying to register with an existing email."""

    status_code = 409
    code = "EMAIL_EXISTS"
    message = "Email address is already registered"


class UsernameAlreadyExistsError(BaseAppException):
    """Raised when trying to register with an existing username."""

    status_code = 409
    code = "USERNAME_EXISTS"
    message = "Username is already taken"
