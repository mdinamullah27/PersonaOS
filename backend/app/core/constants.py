"""Application constants and enums.

Centralizes all constant values used across the application.
"""

from enum import Enum

# Application
APP_TITLE = "PersonaOS"
APP_DESCRIPTION = "AI Digital Twin Platform"


class UserRole(str, Enum):
    """User role definitions for RBAC."""

    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"


class Permission(str, Enum):
    """Permission definitions for RBAC."""

    # User management
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    # Workspace management
    WORKSPACE_CREATE = "workspace:create"
    WORKSPACE_READ = "workspace:read"
    WORKSPACE_UPDATE = "workspace:update"
    WORKSPACE_DELETE = "workspace:delete"

    # Document management
    DOCUMENT_CREATE = "document:create"
    DOCUMENT_READ = "document:read"
    DOCUMENT_UPDATE = "document:update"
    DOCUMENT_DELETE = "document:delete"

    # Chat management
    CHAT_CREATE = "chat:create"
    CHAT_READ = "chat:read"
    CHAT_UPDATE = "chat:update"
    CHAT_DELETE = "chat:delete"

    # Analytics
    ANALYTICS_READ = "analytics:read"

    # Admin
    ADMIN_PANEL = "admin:panel"


# Role-Permission mapping
ROLE_PERMISSIONS: dict[UserRole, list[Permission]] = {
    UserRole.SUPERUSER: list(Permission),  # All permissions
    UserRole.ADMIN: [
        Permission.USER_CREATE,
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
        Permission.WORKSPACE_CREATE,
        Permission.WORKSPACE_READ,
        Permission.WORKSPACE_UPDATE,
        Permission.WORKSPACE_DELETE,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
        Permission.CHAT_CREATE,
        Permission.CHAT_READ,
        Permission.CHAT_UPDATE,
        Permission.CHAT_DELETE,
        Permission.ANALYTICS_READ,
        Permission.ADMIN_PANEL,
    ],
    UserRole.USER: [
        Permission.WORKSPACE_READ,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.CHAT_CREATE,
        Permission.CHAT_READ,
    ],
}



