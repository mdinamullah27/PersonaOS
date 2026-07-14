"""Authentication repository.

Handles database operations for authentication.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class AuthRepository:
    """Repository for authentication-related database operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: Database session.
        """
        self._session = session

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email address.

        Args:
            email: User email.

        Returns:
            User instance or None.
        """
        result = await self._session.execute(
            select(User).where(User.email == email, ~User.is_deleted)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID.

        Returns:
            User instance or None.
        """
        result = await self._session.execute(
            select(User).where(User.id == user_id, ~User.is_deleted)
        )
        return result.scalar_one_or_none()
