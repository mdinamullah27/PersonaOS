"""Create users table

Revision ID: 001_initial
Revises: 
Create Date: 2026-07-14

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Create users table."""
    op.create_table(
        "users",
        # UUID primary key
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
            comment="Unique identifier",
        ),
        # Timestamps
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            comment="Record creation timestamp",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            comment="Record last update timestamp",
        ),
        # Soft delete
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
            comment="Soft delete flag",
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="Soft delete timestamp",
        ),
        # User fields
        sa.Column(
            "email",
            sa.String(255),
            nullable=False,
            comment="User email address",
        ),
        sa.Column(
            "username",
            sa.String(50),
            nullable=False,
            comment="Username",
        ),
        sa.Column(
            "hashed_password",
            sa.String(255),
            nullable=False,
            comment="Hashed password",
        ),
        sa.Column(
            "full_name",
            sa.String(100),
            nullable=True,
            comment="User's full name",
        ),
        sa.Column(
            "role",
            sa.String(20),
            nullable=False,
            server_default="member",
            comment="User role",
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
            comment="Account active status",
        ),
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
            comment="Email verified status",
        ),
        # Constraints
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )

    # Create indexes
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_index(op.f("ix_users_is_deleted"), "users", ["is_deleted"], unique=False)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)


def downgrade() -> None:
    """Downgrade schema - Drop users table."""
    op.drop_table("users")
