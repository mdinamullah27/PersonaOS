"""Health check endpoints.

Provides health, readiness, and version endpoints for monitoring
and container orchestration.
"""

from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.responses import SuccessResponse

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get(
    "/health",
    response_model=SuccessResponse[dict],
    summary="Health check",
    description="Returns application health status.",
)
async def health_check() -> SuccessResponse[dict]:
    """Health check endpoint.

    Returns:
        Application health status.
    """
    return SuccessResponse(
        data={
            "status": "healthy",
            "timestamp": datetime.now(UTC).isoformat(),
        },
        message="Application is healthy",
    )


@router.get(
    "/ready",
    response_model=SuccessResponse[dict],
    summary="Readiness check",
    description="Returns application readiness status including dependency checks.",
)
async def readiness_check() -> SuccessResponse[dict]:
    """Readiness check endpoint.

    Checks connectivity to dependencies (database, Redis).

    Returns:
        Readiness status with dependency health.
    """
    checks: dict[str, str] = {}

    # Database check
    try:
        from app.db.engine import engine

        async with engine.connect() as conn:
            await conn.execute(
                __import__("sqlalchemy", fromlist=["text"]).text("SELECT 1")
            )
        checks["database"] = "healthy"
    except Exception:
        checks["database"] = "unhealthy"

    # Redis check
    try:
        import redis.asyncio as aioredis

        redis_client = aioredis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.aclose()
        checks["redis"] = "healthy"
    except Exception:
        checks["redis"] = "unhealthy"

    all_healthy = all(status == "healthy" for status in checks.values())

    return SuccessResponse(
        data={
            "status": "ready" if all_healthy else "degraded",
            "timestamp": datetime.now(UTC).isoformat(),
            "checks": checks,
        },
        message="Application is ready" if all_healthy else "Some dependencies are unhealthy",
    )


@router.get(
    "/version",
    response_model=SuccessResponse[dict],
    summary="Version info",
    description="Returns application version and environment information.",
)
async def version_info() -> SuccessResponse[dict]:
    """Version information endpoint.

    Returns:
        Application version and environment details.
    """
    return SuccessResponse(
        data={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "python_version": "3.12+",
        },
        message="Version information retrieved",
    )
