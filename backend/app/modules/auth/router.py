"""Authentication router.

Handles login and logout endpoints.
"""

from fastapi import APIRouter, Depends

from app.core.responses import SuccessResponse
from app.modules.auth.dependencies import CurrentUserDep
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service() -> AuthService:
    """Dependency to get auth service.

    Returns:
        AuthService instance.
    """
    from app.db.session import session_factory
    from app.modules.auth.repository import AuthRepository

    repository = AuthRepository(session_factory())
    return AuthService(repository=repository)


@router.post(
    "/login",
    response_model=SuccessResponse[TokenResponse],
    summary="User login",
    description="Authenticate user with email and password.",
)
async def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[TokenResponse]:
    """Login endpoint.

    Authenticates a user and returns JWT tokens.
    """
    token_response = await service.authenticate(data)
    return SuccessResponse(
        data=token_response,
        message="Login successful",
    )


@router.post(
    "/logout",
    response_model=SuccessResponse,
    summary="User logout",
    description="Logout and invalidate tokens.",
)
async def logout(
    current_user: CurrentUserDep,
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse:
    """Logout endpoint.

    Invalidates the current user's tokens.
    """
    await service.logout(str(current_user.id))
    return SuccessResponse(message="Logout successful")
