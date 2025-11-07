"""Tests for authentication routes."""
import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.integration
class TestAuthRoutes:
    """Test authentication routes."""

    async def test_login_form_data_success(self, async_client: AsyncClient, test_user: User):
        """Test login with form data (OAuth2)."""
        response = await async_client.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpass123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_form_data_wrong_credentials(
        self, async_client: AsyncClient, test_user: User
    ):
        """Test login with wrong credentials."""
        response = await async_client.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    async def test_login_json_success(self, async_client: AsyncClient, test_user: User):
        """Test login with JSON body."""
        response = await async_client.post(
            "/auth/login/json",
            json={"username": "testuser", "password": "testpass123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_json_wrong_credentials(
        self, async_client: AsyncClient, test_user: User
    ):
        """Test JSON login with wrong credentials."""
        response = await async_client.post(
            "/auth/login/json",
            json={"username": "testuser", "password": "wrongpassword"},
        )

        assert response.status_code == 401

    async def test_login_json_nonexistent_user(self, async_client: AsyncClient):
        """Test JSON login with nonexistent user."""
        response = await async_client.post(
            "/auth/login/json",
            json={"username": "nonexistent", "password": "password"},
        )

        assert response.status_code == 401

    async def test_get_current_user_success(
        self, async_client: AsyncClient, test_user: User, user_token: str
    ):
        """Test getting current user info."""
        response = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True
        assert data["is_admin"] is False

    async def test_get_current_user_no_token(self, async_client: AsyncClient):
        """Test getting current user without token."""
        response = await async_client.get("/auth/me")

        assert response.status_code == 401

    async def test_get_current_user_invalid_token(self, async_client: AsyncClient):
        """Test getting current user with invalid token."""
        response = await async_client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    async def test_get_current_user_malformed_header(self, async_client: AsyncClient):
        """Test getting current user with malformed auth header."""
        response = await async_client.get(
            "/auth/me",
            headers={"Authorization": "InvalidFormat token123"},
        )

        assert response.status_code == 401
