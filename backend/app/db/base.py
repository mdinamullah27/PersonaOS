"""Base model configuration for all database models.

Provides the base model class with common mixins for UUID primary keys,
timestamps, and soft delete functionality.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.mixins import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class BaseModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Abstract base model for all database models.

    Includes:
        - UUID primary key
        - created_at and updated_at timestamps
        - Soft delete functionality

    All application models should inherit from this class.

    Example:
        class User(BaseModel):
            __tablename__ = "users"
            name: Mapped[str]
    """

    __abstract__ = True

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self) -> dict:
        """Convert model instance to dictionary.

        Returns:
            Dictionary representation of the model.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
