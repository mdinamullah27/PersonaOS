"""Users router.

Handles user management endpoints.
"""

from fastapi import APIRouter, Depends, Query

from app.core.constants import PaginationDefaults, Permission
from app.core.responses import SuccessResponse
from app.modules.auth.dependencies import CurrentUserDep, require_permissions
from app.modules.users.schemas import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=SuccessResponse[dict],
    summary="List users",
    description="Get a paginated list of users.",
    dependencies=[Depends(require_permissions(Permission.USER_READ))],
)
async def list_users(
    current_user: CurrentUserDep,
    page: int = Query(default=int(PaginationDefaults.PAGE.value), ge=1),
    page_size: int = Query(default=int(PaginationDefaults.PAGE_SIZE.value), ge=1, le=100),
) -> SuccessResponse[dict]:
    """List users endpoint.

    Returns a paginated list of users.
    """
    # Phase 2: Implement with service
    return SuccessResponse(
        data={
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "pages": 0,
        },
        message="Users retrieved successfully",
    )


@router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
    summary="Get current user profile",
    description="Get the authenticated user's profile.",
)
async def get_current_user_profile(
    current_user: CurrentUserDep,
) -> SuccessResponse[UserResponse]:
    """Get current user profile endpoint."""
    # Phase 2: Implement with service
    return SuccessResponse(
        data=UserResponse(
            id=current_user.id,
            email=current_user.email,
            username=current_user.username,
            full_name=None,
            role=current_user.role,
            is_active=current_user.is_active,
            is_verified=False,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        ),
        message="Profile retrieved successfully",
    )


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    summary="Get user by ID",
    description="Get a specific user by their ID.",
    dependencies=[Depends(require_permissions(Permission.USER_READ))],
)
async def get_user(
    user_id: str,
    current_user: CurrentUserDep,
) -> SuccessResponse[UserResponse]:
    """Get user by ID endpoint."""
    # Phase 2: Implement with service
    return SuccessResponse(
        data=UserResponse(
            id=user_id,
            email="user@example.com",
            username="user",
            full_name=None,
            role="member",
            is_active=True,
            is_verified=False,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        ),
        message="User retrieved successfully",
    )


@router.patch(
    "/me",
    response_model=SuccessResponse[UserResponse],
    summary="Update current user",
    description="Update the authenticated user's profile.",
)
async def update_current_user(
    data: UserUpdate,
    current_user: CurrentUserDep,
) -> SuccessResponse[UserResponse]:
    """Update current user profile endpoint."""
    # Phase 2: Implement with service
    return SuccessResponse(
        data=UserResponse(
            id=current_user.id,
            email=current_user.email,
            username=current_user.username,
            full_name=data.full_name,
            role=current_user.role,
            is_active=current_user.is_active,
            is_verified=False,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        ),
        message="Profile updated successfully",
    )
