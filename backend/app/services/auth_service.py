from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
)
from app.models.user import User
from app.schemas.user import Token


class AuthService:
    """Authentication service."""

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = await User.filter(username=username).first()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return user

    @staticmethod
    async def login(username: str, password: str) -> Token:
        """Login a user and return access token."""
        user = await AuthService.authenticate_user(username, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    async def get_current_user(token: str) -> User:
        """Get current user from token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = await User.filter(username=username).first()
        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    async def get_current_active_user(token: str) -> User:
        """Get current active user from token."""
        user = await AuthService.get_current_user(token)

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )

        return user

    @staticmethod
    async def get_current_admin_user(token: str) -> User:
        """Get current admin user from token."""
        user = await AuthService.get_current_active_user(token)

        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return user
