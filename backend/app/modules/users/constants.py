"""User module constants.

Defines constants for the users module.
"""

from app.core.constants import UserRole

# Default role for new users
DEFAULT_USER_ROLE = UserRole.MEMBER

# Username constraints
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
USERNAME_PATTERN = r"^[a-zA-Z0-9_-]+$"
