"""Exception hierarchy and global exception handlers.

Provides a structured exception system for the application with
proper HTTP status codes and error responses.
"""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.logging import log_exception
from app.core.responses import ErrorResponse


class BaseAppException(Exception):
    """Base exception for all application exceptions.

    Attributes:
        status_code: HTTP status code for the error.
        message: Human-readable error message.
        code: Application-specific error code.
        details: Additional error details.
    """

    status_code: int = 500
    code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Optional custom error message.
            details: Optional additional error details.
        """
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary representation.

        Returns:
            Dictionary containing error information.
        """
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class NotFoundException(BaseAppException):
    """Resource not found exception."""

    status_code = 404
    code = "NOT_FOUND"
    message = "The requested resource was not found"


class ForbiddenException(BaseAppException):
    """Insufficient permissions exception."""

    status_code = 403
    code = "FORBIDDEN"
    message = "You do not have permission to perform this action"


class UnauthorizedException(BaseAppException):
    """Authentication required exception."""

    status_code = 401
    code = "UNAUTHORIZED"
    message = "Authentication is required"


class ConflictException(BaseAppException):
    """Resource conflict exception."""

    status_code = 409
    code = "CONFLICT"
    message = "The request conflicts with an existing resource"


class ValidationException(BaseAppException):
    """Validation error exception."""

    status_code = 422
    code = "VALIDATION_ERROR"
    message = "The request data is invalid"


class BusinessRuleException(BaseAppException):
    """Business rule violation exception."""

    status_code = 400
    code = "BUSINESS_RULE_VIOLATION"
    message = "The request violates a business rule"


class RateLimitException(BaseAppException):
    """Rate limit exceeded exception."""

    status_code = 429
    code = "RATE_LIMITED"
    message = "Too many requests, please try again later"


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app.

    Args:
        app: FastAPI application instance.
    """

    @app.exception_handler(BaseAppException)
    async def base_app_exception_handler(
        request: Request,
        exc: BaseAppException,
    ) -> JSONResponse:
        """Handle all application-specific exceptions."""
        log_exception(exc, path=request.url.path, method=request.method)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                success=False,
                message=exc.message,
                code=exc.code,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Handle FastAPI request validation errors."""
        errors = exc.errors()
        details = {}
        for error in errors:
            loc = ".".join(str(loc) for loc in error.get("loc", []))
            details[loc] = error.get("msg", "Validation error")

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                success=False,
                message="Request validation failed",
                code="VALIDATION_ERROR",
                details=details,
            ).model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                success=False,
                message="Data validation failed",
                code="VALIDATION_ERROR",
                details={"errors": exc.errors()},
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle all unhandled exceptions."""
        log_exception(exc, path=request.url.path, method=request.method)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                success=False,
                message="An internal server error occurred",
                code="INTERNAL_ERROR",
            ).model_dump(),
        )
