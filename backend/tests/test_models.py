"""Tests for database models and mixins.

Tests model creation, mixins, and base model functionality.
"""

import uuid
from datetime import UTC, datetime

import pytest

from app.modules.users.models import User


@pytest.mark.unit
class TestUserModel:
    """Test User model."""

    def test_user_model_has_correct_tablename(self) -> None:
        """Test User model table name."""
        assert User.__tablename__ == "users"

    def test_user_model_columns(self) -> None:
        """Test User model has required columns."""
        columns = [col.name for col in User.__table__.columns]

        assert "id" in columns
        assert "email" in columns
        assert "username" in columns
        assert "hashed_password" in columns
        assert "full_name" in columns
        assert "role" in columns
        assert "is_active" in columns
        assert "is_verified" in columns
        assert "created_at" in columns
        assert "updated_at" in columns
        assert "is_deleted" in columns
        assert "deleted_at" in columns

    def test_user_model_repr(self) -> None:
        """Test User model string representation."""
        user = User.__new__(User)
        user.id = uuid.uuid4()
        user.email = "test@example.com"
        user.username = "testuser"

        repr_str = repr(user)
        assert "User" in repr_str
        assert str(user.id) in repr_str


@pytest.mark.unit
class TestModelMixins:
    """Test model mixins functionality."""

    def test_soft_delete_mixin_has_methods(self) -> None:
        """Test SoftDeleteMixin has soft_delete and restore methods."""
        from app.db.mixins import SoftDeleteMixin

        assert hasattr(SoftDeleteMixin, "soft_delete")
        assert hasattr(SoftDeleteMixin, "restore")

    def test_soft_delete_sets_flags(self) -> None:
        """Test soft_delete sets is_deleted and deleted_at."""
        from app.db.mixins import SoftDeleteMixin

        class TestModel(SoftDeleteMixin):
            def __init__(self) -> None:
                self.is_deleted = False
                self.deleted_at = None

        model = TestModel()
        model.soft_delete()

        assert model.is_deleted is True
        assert model.deleted_at is not None

    def test_restore_clears_flags(self) -> None:
        """Test restore clears is_deleted and deleted_at."""
        from app.db.mixins import SoftDeleteMixin

        class TestModel(SoftDeleteMixin):
            def __init__(self) -> None:
                self.is_deleted = True
                self.deleted_at = datetime.now(UTC)

        model = TestModel()
        model.restore()

        assert model.is_deleted is False
        assert model.deleted_at is None
