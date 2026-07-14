"""Database dependencies for FastAPI dependency injection.

Provides database session and repository dependencies.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency.

    Yields:
        AsyncSession: Database session.
    """
    async for session in get_session():
        yield session


# Type annotation for database session dependency
DBSession = Annotated[AsyncSession, Depends(get_db)]
