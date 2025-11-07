from typing import List, Optional

from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User service for CRUD operations."""

    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if username already exists
        existing_user = await User.filter(username=user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Check if email already exists
        existing_email = await User.filter(email=user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user
        user = await User.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            is_admin=user_data.is_admin,
        )

        return user

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        user = await User.filter(id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        user = await User.filter(username=username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        users = await User.all().offset(skip).limit(limit)
        return users

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> User:
        """Update a user."""
        user = await UserService.get_user_by_id(user_id)

        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)

        if "username" in update_data:
            # Check if new username is already taken
            existing = await User.filter(username=update_data["username"]).first()
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken",
                )
            user.username = update_data["username"]

        if "email" in update_data:
            # Check if new email is already taken
            existing = await User.filter(email=update_data["email"]).first()
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already taken",
                )
            user.email = update_data["email"]

        if "password" in update_data:
            user.hashed_password = get_password_hash(update_data["password"])

        if "is_active" in update_data:
            user.is_active = update_data["is_active"]

        if "is_admin" in update_data:
            user.is_admin = update_data["is_admin"]

        await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: int) -> None:
        """Delete a user."""
        user = await UserService.get_user_by_id(user_id)
        await user.delete()
