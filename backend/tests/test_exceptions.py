"""Tests for exception handling.

Tests the exception hierarchy and error responses.
"""

import pytest

from app.core.exceptions import (
    BaseAppException,
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    RateLimitException,
    UnauthorizedException,
    ValidationException,
)


@pytest.mark.unit
class TestExceptionHierarchy:
    """Test exception class hierarchy."""

    def test_base_exception_is_exception(self) -> None:
        """Test BaseAppException inherits from Exception."""
        assert issubclass(BaseAppException, Exception)

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test all custom exceptions inherit from BaseAppException."""
        exceptions = [
            NotFoundException,
            ForbiddenException,
            UnauthorizedException,
            ConflictException,
            ValidationException,
            BusinessRuleException,
            RateLimitException,
        ]

        for exc_class in exceptions:
            assert issubclass(exc_class, BaseAppException)


@pytest.mark.unit
class TestExceptionAttributes:
    """Test exception attributes and methods."""

    def test_not_found_exception_attributes(self) -> None:
        """Test NotFoundException has correct attributes."""
        exc = NotFoundException()

        assert exc.status_code == 404
        assert exc.code == "NOT_FOUND"
        assert "not found" in exc.message.lower()

    def test_forbidden_exception_attributes(self) -> None:
        """Test ForbiddenException has correct attributes."""
        exc = ForbiddenException()

        assert exc.status_code == 403
        assert exc.code == "FORBIDDEN"

    def test_unauthorized_exception_attributes(self) -> None:
        """Test UnauthorizedException has correct attributes."""
        exc = UnauthorizedException()

        assert exc.status_code == 401
        assert exc.code == "UNAUTHORIZED"

    def test_conflict_exception_attributes(self) -> None:
        """Test ConflictException has correct attributes."""
        exc = ConflictException()

        assert exc.status_code == 409
        assert exc.code == "CONFLICT"

    def test_validation_exception_attributes(self) -> None:
        """Test ValidationException has correct attributes."""
        exc = ValidationException()

        assert exc.status_code == 422
        assert exc.code == "VALIDATION_ERROR"

    def test_custom_message(self) -> None:
        """Test exception with custom message."""
        custom_msg = "Custom error message"
        exc = NotFoundException(message=custom_msg)

        assert exc.message == custom_msg

    def test_exception_with_details(self) -> None:
        """Test exception with details dictionary."""
        details = {"field": "email", "reason": "already exists"}
        exc = ConflictException(details=details)

        assert exc.details == details

    def test_to_dict_method(self) -> None:
        """Test to_dict method returns proper structure."""
        exc = NotFoundException(message="Not found", details={"id": "123"})
        result = exc.to_dict()

        assert isinstance(result, dict)
        assert result["code"] == "NOT_FOUND"
        assert result["message"] == "Not found"
        assert result["details"] == {"id": "123"}

    def test_exception_is_picklable(self) -> None:
        """Test exception can be serialized."""
        import pickle

        exc = NotFoundException(message="Test error")
        pickled = pickle.dumps(exc)
        unpickled = pickle.loads(pickled)

        assert unpickled.message == exc.message
        assert unpickled.status_code == exc.status_code
