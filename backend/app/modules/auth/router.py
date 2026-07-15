"""Authentication router.

Handles login and logout endpoints.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.responses import SuccessResponse
from app.modules.auth.dependencies import CurrentUserDep
from app.modules.auth.schemas import TokenResponse
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
    response_model=TokenResponse,
    summary="User login",
    description="Authenticate user with email and password.",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Login endpoint.

    Authenticates a user and returns JWT tokens.
    """
    return await service.authenticate(
        email=form_data.username,
        password=form_data.password,
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
    return SuccessResponse(
        data={"status": "logged_out"},
        message="Logout successful",
    )
