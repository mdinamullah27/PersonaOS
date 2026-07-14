"""Authentication module exceptions.

Re-exports exceptions from the auth module for convenience.
"""

from app.modules.auth.exceptions import (
    AccountDisabledError,
    AccountLockedError,
    AuthenticationError,
    EmailAlreadyExistsError,
    InsufficientPermissionsError,
    InvalidTokenError,
    TokenExpiredError,
    UsernameAlreadyExistsError,
)

__all__ = [
    "AccountDisabledError",
    "AccountLockedError",
    "AuthenticationError",
    "EmailAlreadyExistsError",
    "InsufficientPermissionsError",
    "InvalidTokenError",
    "TokenExpiredError",
    "UsernameAlreadyExistsError",
]
