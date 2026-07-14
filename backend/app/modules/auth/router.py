"""Authentication router.

Handles authentication endpoints including login, registration,
and token refresh.
"""

from fastapi import APIRouter, Depends

from app.core.responses import SuccessResponse
from app.modules.auth.dependencies import CurrentUserDep
from app.modules.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service() -> AuthService:
    """Dependency to get auth service.

    Returns:
        AuthService instance.
    """
    # Phase 2: Inject repository with database session
    from app.modules.auth.repository import AuthRepository

    repository = AuthRepository(session=None)  # Type: ignore
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
    "/register",
    response_model=SuccessResponse[dict],
    summary="User registration",
    description="Register a new user account.",
)
async def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[dict]:
    """Registration endpoint.

    Creates a new user account.
    """
    user_data = await service.register(data)
    return SuccessResponse(
        data=user_data,
        message="Registration successful",
    )


@router.post(
    "/refresh",
    response_model=SuccessResponse[TokenResponse],
    summary="Refresh access token",
    description="Get new tokens using a refresh token.",
)
async def refresh_token(
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[TokenResponse]:
    """Token refresh endpoint.

    Exchanges a refresh token for new access and refresh tokens.
    """
    token_response = await service.refresh_tokens(data.refresh_token)
    return SuccessResponse(
        data=token_response,
        message="Token refreshed successfully",
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
    await service.logout(current_user.id)
    return SuccessResponse(message="Logout successful")


@router.get(
    "/me",
    response_model=SuccessResponse[dict],
    summary="Get current user",
    description="Get the authenticated user's profile.",
)
async def get_me(
    current_user: CurrentUserDep,
) -> SuccessResponse[dict]:
    """Get current user endpoint.

    Returns the authenticated user's information.
    """
    return SuccessResponse(
        data={
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "role": current_user.role,
        },
        message="User profile retrieved",
    )
