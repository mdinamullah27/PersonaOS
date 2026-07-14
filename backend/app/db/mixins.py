"""SQLAlchemy model mixins.

Provides reusable mixins for common model patterns:
- TimestampMixin: created_at, updated_at fields
- UUIDPrimaryKeyMixin: UUID-based primary key
- SoftDeleteMixin: Soft delete functionality
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    Provides common functionality for all models.
    """

    pass


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps.

    Automatically manages creation and update timestamps.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Record last update timestamp",
    )


class UUIDPrimaryKeyMixin:
    """Mixin that adds a UUID primary key.

    Uses PostgreSQL UUID type with automatic UUID generation.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier",
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete functionality.

    Records are not physically deleted but marked as deleted.
    """

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        index=True,
        comment="Soft delete flag",
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Soft delete timestamp",
    )

    def soft_delete(self) -> None:
        """Mark the record as deleted."""
        from datetime import datetime

        self.is_deleted = True
        self.deleted_at = datetime.now(UTC)

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
