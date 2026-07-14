"""User database models.

Defines the User model for database storage.
"""


from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import UserRole
from app.db.base import BaseModel


class User(BaseModel):
    """User model.

    Stores user account information and authentication credentials.

    Attributes:
        id: UUID primary key.
        email: Unique email address.
        username: Unique username.
        hashed_password: Hashed password.
        full_name: User's full name.
        role: User role for RBAC.
        is_active: Whether account is active.
        is_verified: Whether email is verified.
        is_deleted: Soft delete flag.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="User email address",
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Username",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Hashed password",
    )
    full_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="User's full name",
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False),
        default=UserRole.USER,
        nullable=False,
        comment="User role",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Account active status",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Email verified status",
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
