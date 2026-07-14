"""Async SQLAlchemy engine configuration.

Provides the async database engine with connection pooling.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_settings

settings = get_settings()


def create_engine() -> AsyncEngine:
    """Create an async SQLAlchemy engine.

    Returns:
        Configured async engine instance.
    """
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,
        pool_recycle=3600,
    )


engine: AsyncEngine = create_engine()
