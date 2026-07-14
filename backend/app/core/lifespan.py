"""Application lifespan manager.

Handles startup and shutdown events for database connections,
Redis, and other services.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from sqlalchemy import select

from app.core.config import get_settings
from app.core.security import hash_password

logger = structlog.get_logger()
settings = get_settings()


async def seed_superadmin() -> None:
    """Seed the superadmin user from .env credentials if not exists."""
    from app.core.constants import UserRole
    from app.db.session import session_factory
    from app.modules.users.models import User

    async with session_factory() as session:
        result = await session.execute(select(User).where(User.email == settings.SUPERUSER_EMAIL))
        existing = result.scalar_one_or_none()

        if existing:
            logger.info("superuser_already_exists", email=settings.SUPERUSER_EMAIL)
            return

        superuser = User(
            email=settings.SUPERUSER_EMAIL,
            username="superuser",
            hashed_password=hash_password(settings.SUPERUSER_PASSWORD),
            full_name="Superuser",
            role=UserRole.SUPERUSER,
            is_active=True,
            is_verified=True,
        )
        session.add(superuser)
        await session.commit()

        logger.info(
            "superuser_created",
            email=settings.SUPERUSER_EMAIL,
            role=UserRole.SUPERUSER.value,
        )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifecycle events.

    Handles initialization and cleanup of application resources.

    Args:
        app: FastAPI application instance.

    Yields:
        None: Application runs during yield.
    """
    # Startup
    logger.info(
        "application_starting",
        app_name=settings.APP_NAME,
        environment=settings.ENVIRONMENT,
        debug=settings.DEBUG,
    )

    # Seed superuser from .env
    try:
        await seed_superadmin()
    except Exception as exc:
        logger.error("superuser_seed_failed", error=str(exc))

    yield

    # Shutdown
    logger.info("application_shutting_down")
