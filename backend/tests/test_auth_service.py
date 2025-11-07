"""Tests for authentication service."""
import pytest
from fastapi import HTTPException

from app.models.user import User
from app.services.auth_service import AuthService


@pytest.mark.unit
class TestAuthService:
    """Test authentication service."""

    async def test_authenticate_user_success(self, test_user: User):
        """Test successful user authentication."""
        user = await AuthService.authenticate_user("testuser", "testpass123")
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    async def test_authenticate_user_wrong_password(self, test_user: User):
        """Test authentication with wrong password."""
        user = await AuthService.authenticate_user("testuser", "wrongpassword")
        assert user is None

    async def test_authenticate_user_nonexistent(self):
        """Test authentication with nonexistent user."""
        user = await AuthService.authenticate_user("nonexistent", "password")
        assert user is None

    async def test_authenticate_inactive_user(self, inactive_user: User):
        """Test authentication with inactive user."""
        user = await AuthService.authenticate_user("inactive", "inactive123")
        assert user is None

    async def test_login_success(self, test_user: User):
        """Test successful login."""
        token = await AuthService.login("testuser", "testpass123")
        assert token.access_token is not None
        assert token.token_type == "bearer"

    async def test_login_wrong_credentials(self, test_user: User):
        """Test login with wrong credentials."""
        with pytest.raises(HTTPException) as exc:
            await AuthService.login("testuser", "wrongpassword")
        assert exc.value.status_code == 401
        assert "Incorrect username or password" in str(exc.value.detail)

    async def test_login_nonexistent_user(self):
        """Test login with nonexistent user."""
        with pytest.raises(HTTPException) as exc:
            await AuthService.login("nonexistent", "password")
        assert exc.value.status_code == 401

    async def test_get_current_user_success(self, test_user: User, user_token: str):
        """Test getting current user with valid token."""
        user = await AuthService.get_current_user(user_token)
        assert user is not None
        assert user.username == "testuser"

    async def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token."""
        with pytest.raises(HTTPException) as exc:
            await AuthService.get_current_user("invalid_token")
        assert exc.value.status_code == 401
        assert "Could not validate credentials" in str(exc.value.detail)

    async def test_get_current_active_user_success(self, test_user: User, user_token: str):
        """Test getting current active user."""
        user = await AuthService.get_current_active_user(user_token)
        assert user is not None
        assert user.username == "testuser"
        assert user.is_active is True

    async def test_get_current_admin_user_success(self, test_admin: User, admin_token: str):
        """Test getting current admin user."""
        user = await AuthService.get_current_admin_user(admin_token)
        assert user is not None
        assert user.username == "admin"
        assert user.is_admin is True

    async def test_get_current_admin_user_not_admin(self, test_user: User, user_token: str):
        """Test getting admin user with non-admin token."""
        with pytest.raises(HTTPException) as exc:
            await AuthService.get_current_admin_user(user_token)
        assert exc.value.status_code == 403
        assert "Not enough permissions" in str(exc.value.detail)
