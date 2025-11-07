from typing import List

from fastapi import APIRouter, Depends, status

from app.routes.auth import oauth2_scheme
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["Admin"])


async def get_current_admin_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current admin user from token."""
    return await AuthService.get_current_admin_user(token)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_admin=Depends(get_current_admin_user),
):
    """
    Create a new user (Admin only).

    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (minimum 4 characters)
    - **is_admin**: Whether the user should be an admin (default: false)
    """
    user = await UserService.create_user(user_data)
    return user


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_admin=Depends(get_current_admin_user),
):
    """
    Get all users with pagination (Admin only).

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    users = await UserService.get_all_users(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_admin=Depends(get_current_admin_user),
):
    """
    Get a specific user by ID (Admin only).

    - **user_id**: User's ID
    """
    user = await UserService.get_user_by_id(user_id)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_admin=Depends(get_current_admin_user),
):
    """
    Update a user (Admin only).

    - **user_id**: User's ID
    - **username**: New username (optional)
    - **email**: New email (optional)
    - **password**: New password (optional)
    - **is_active**: Active status (optional)
    - **is_admin**: Admin status (optional)
    """
    user = await UserService.update_user(user_id, user_data)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_admin=Depends(get_current_admin_user),
):
    """
    Delete a user (Admin only).

    - **user_id**: User's ID
    """
    await UserService.delete_user(user_id)
    return None
