"""Authentication service.

Business logic for authentication workflows.
"""

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.modules.auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.modules.auth.exceptions import (
    AuthenticationError,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
)


class AuthService:
    """Service for authentication business logic.

    Handles login and token management.
    """

    def __init__(self, repository: AuthRepository) -> None:
        """Initialize the service.

        Args:
            repository: Authentication repository.
        """
        self._repository = repository

    async def authenticate(self, data: LoginRequest) -> TokenResponse:
        """Authenticate user with email and password.

        Args:
            data: Login credentials.

        Returns:
            TokenResponse with access token.

        Raises:
            AuthenticationError: If credentials are invalid.
        """
        user = await self._repository.get_user_by_email(data.email)
        if not user:
            raise AuthenticationError(message="Invalid email or password")

        if not verify_password(data.password, user.hashed_password):
            raise AuthenticationError(message="Invalid email or password")

        if not user.is_active:
            raise AuthenticationError(message="Account is disabled")

        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={
                "email": user.email,
                "username": user.username,
                "role": user.role.value,
            },
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def logout(self, user_id: str) -> None:
        """Logout user.

        Args:
            user_id: User ID.
        """
        pass
