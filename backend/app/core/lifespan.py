"""Application lifespan manager.

Handles startup and shutdown events for database connections,
Redis, and other services.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.core.config import get_settings

logger = structlog.get_logger()
settings = get_settings()


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

    # Initialize services here in future phases:
    # - Database connection pool
    # - Redis connection
    # - Celery worker
    # - AI providers

    yield

    # Shutdown
    logger.info("application_shutting_down")

    # Cleanup services here in future phases:
    # - Close database connections
    # - Close Redis connection
    # - Shutdown Celery worker
