from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.schemas.user import Token, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from token."""
    return await AuthService.get_current_active_user(token)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint - returns JWT token.

    - **username**: User's username
    - **password**: User's password
    """
    token = await AuthService.login(form_data.username, form_data.password)
    return token


@router.post("/login/json", response_model=Token)
async def login_json(user_data: UserLogin):
    """
    Login endpoint with JSON body - returns JWT token.

    - **username**: User's username
    - **password**: User's password
    """
    token = await AuthService.login(user_data.username, user_data.password)
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user=Depends(get_current_user)):
    """
    Get current user information.

    Requires authentication token.
    """
    return current_user
