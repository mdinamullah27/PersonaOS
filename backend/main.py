"""PersonaOS - AI Digital Twin Platform.

Enterprise backend for AI-powered digital twin management.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.core.middleware import (
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
    TimingMiddleware,
)

settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Middleware (order matters - last added = first executed)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    register_exception_handlers(app)

    # Register Routers
    _register_routers(app)

    return app


def _register_routers(app: FastAPI) -> None:
    """Register all API routers.

    Args:
        app: FastAPI application instance.
    """
    from app.api.v1.health import router as health_router
    from app.modules.auth.router import router as auth_router
    from app.modules.users.router import router as users_router

    # Health endpoints (no prefix)
    app.include_router(health_router)

    # API v1 routers
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(users_router, prefix=settings.API_V1_PREFIX)


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
