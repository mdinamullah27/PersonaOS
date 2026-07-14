"""Authentication constants.

Defines authentication-related constants and configurations.
"""

# Token configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Token types
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# Header
AUTH_HEADER_NAME = "Authorization"
AUTH_HEADER_PREFIX = "Bearer"

# Password requirements
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
