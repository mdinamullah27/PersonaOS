"""Tests for security utilities.

Tests JWT token creation/validation and password hashing.
"""

import pytest

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


@pytest.mark.unit
class TestJWT:
    """Test JWT token operations."""

    def test_create_access_token(self) -> None:
        """Test creating a JWT access token."""
        token = create_access_token(subject="user123")

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self) -> None:
        """Test decoding a valid JWT token."""
        user_id = "user123"
        token = create_access_token(subject=user_id)
        payload = decode_token(token)

        assert payload["sub"] == user_id
        assert payload["type"] == "access"

    def test_decode_expired_token(self) -> None:
        """Test decoding an expired token raises error."""
        from datetime import timedelta

        import jwt

        token = create_access_token(
            subject="user123",
            expires_delta=timedelta(seconds=-1),
        )

        with pytest.raises(jwt.ExpiredSignatureError):
            decode_token(token)

    def test_decode_invalid_token(self) -> None:
        """Test decoding an invalid token raises error."""
        import jwt

        with pytest.raises(jwt.InvalidTokenError):
            decode_token("invalid.token.here")

    def test_token_with_extra_claims(self) -> None:
        """Test creating token with extra claims."""
        extra_claims = {"role": "admin", "email": "admin@example.com"}
        token = create_access_token(subject="user123", extra_claims=extra_claims)
        payload = decode_token(token)

        assert payload["role"] == "admin"
        assert payload["email"] == "admin@example.com"


@pytest.mark.unit
class TestPasswordHashing:
    """Test password hashing operations."""

    def test_hash_password(self) -> None:
        """Test hashing a password."""
        password = "securepassword123"
        hashed = hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_correct_password(self) -> None:
        """Test verifying correct password."""
        password = "securepassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self) -> None:
        """Test verifying incorrect password."""
        password = "securepassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_same_password_different_hashes(self) -> None:
        """Test that same password produces different hashes (bcrypt salt)."""
        password = "securepassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Different due to random salt
        assert hash1 != hash2
        # But both verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
