"""Structured logging configuration for PersonaOS.

Provides JSON and console logging formats with request/response
correlation IDs for distributed tracing.
"""

import logging
import sys
from typing import Any

import structlog
from fastapi import Request, Response

from app.core.config import get_settings

settings = get_settings()


def setup_logging() -> None:
    """Configure structured logging for the application.

    Sets up structlog with appropriate processors based on environment.
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.LOG_FORMAT == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logging.root.handlers.clear()
    logging.root.addHandler(handler)
    logging.root.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DATABASE_ECHO else logging.WARNING
    )


def bind_request_logger(request: Request, logger: Any) -> Any:
    """Bind request context to logger.

    Args:
        request: FastAPI request object.
        logger: Structlog logger instance.

    Returns:
        Bound logger with request context.
    """
    return logger.bind(
        request_id=request.state.request_id if hasattr(request.state, "request_id") else None,
        method=request.method,
        path=request.url.path,
    )


def log_request(request: Request, body: bytes | None = None) -> None:
    """Log incoming request details.

    Args:
        request: FastAPI request object.
        body: Request body bytes.
    """
    logger = structlog.get_logger("http")
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        query=str(request.query_params),
        client=f"{request.client.host}:{request.client.port}" if request.client else None,
        content_length=request.headers.get("content-length"),
    )


def log_response(
    request: Request,
    response: Response,
    duration_ms: float,
) -> None:
    """Log response details.

    Args:
        request: FastAPI request object.
        response: FastAPI response object.
        duration_ms: Request processing duration in milliseconds.
    """
    logger = structlog.get_logger("http")
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(duration_ms, 2),
    )


def log_exception(exc: Exception, **kwargs: Any) -> None:
    """Log exception with context.

    Args:
        exc: Exception instance.
        **kwargs: Additional context fields.
    """
    logger = structlog.get_logger("exception")
    logger.error(
        "exception_occurred",
        exc_type=type(exc).__name__,
        exc_msg=str(exc),
        **kwargs,
    )
