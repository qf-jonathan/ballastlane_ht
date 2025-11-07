"""Tests for admin routes."""
import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.integration
class TestAdminRoutes:
    """Test admin routes."""

    async def test_create_user_as_admin(self, async_client: AsyncClient, admin_token: str):
        """Test creating a user as admin."""
        response = await async_client.post(
            "/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "is_admin": False,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert data["is_active"] is True
        assert data["is_admin"] is False

    async def test_create_user_as_non_admin(
        self, async_client: AsyncClient, user_token: str
    ):
        """Test creating a user as non-admin (should fail)."""
        response = await async_client.post(
            "/admin/users",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "is_admin": False,
            },
        )

        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]

    async def test_create_user_without_auth(self, async_client: AsyncClient):
        """Test creating a user without authentication."""
        response = await async_client.post(
            "/admin/users",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "is_admin": False,
            },
        )

        assert response.status_code == 401

    async def test_get_all_users_as_admin(
        self, async_client: AsyncClient, test_user: User, test_admin: User, admin_token: str
    ):
        """Test getting all users as admin."""
        response = await async_client.get(
            "/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    async def test_get_all_users_pagination(
        self, async_client: AsyncClient, test_user: User, test_admin: User, admin_token: str
    ):
        """Test getting users with pagination."""
        response = await async_client.get(
            "/admin/users?skip=0&limit=1",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    async def test_get_all_users_as_non_admin(
        self, async_client: AsyncClient, user_token: str
    ):
        """Test getting all users as non-admin (should fail)."""
        response = await async_client.get(
            "/admin/users",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    async def test_get_user_by_id_as_admin(
        self, async_client: AsyncClient, test_user: User, admin_token: str
    ):
        """Test getting user by ID as admin."""
        response = await async_client.get(
            f"/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["id"] == test_user.id

    async def test_get_user_by_id_not_found(
        self, async_client: AsyncClient, admin_token: str
    ):
        """Test getting nonexistent user by ID."""
        response = await async_client.get(
            "/admin/users/9999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404

    async def test_update_user_as_admin(
        self, async_client: AsyncClient, test_user: User, admin_token: str
    ):
        """Test updating user as admin."""
        response = await async_client.put(
            f"/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"username": "updateduser", "is_admin": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updateduser"
        assert data["is_admin"] is True

    async def test_update_user_email(
        self, async_client: AsyncClient, test_user: User, admin_token: str
    ):
        """Test updating user email."""
        response = await async_client.put(
            f"/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"email": "newemail@example.com"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"

    async def test_update_user_password(
        self, async_client: AsyncClient, test_user: User, admin_token: str
    ):
        """Test updating user password."""
        response = await async_client.put(
            f"/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"password": "newpassword123"},
        )

        assert response.status_code == 200
        # Password should be updated (can't directly check hash)
        data = response.json()
        assert data["id"] == test_user.id

    async def test_update_user_as_non_admin(
        self, async_client: AsyncClient, test_admin: User, user_token: str
    ):
        """Test updating user as non-admin (should fail)."""
        response = await async_client.put(
            f"/admin/users/{test_admin.id}",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"username": "hacked"},
        )

        assert response.status_code == 403

    async def test_update_user_not_found(
        self, async_client: AsyncClient, admin_token: str
    ):
        """Test updating nonexistent user."""
        response = await async_client.put(
            "/admin/users/9999",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"username": "updateduser"},
        )

        assert response.status_code == 404

    async def test_delete_user_as_admin(
        self, async_client: AsyncClient, test_user: User, admin_token: str
    ):
        """Test deleting user as admin."""
        response = await async_client.delete(
            f"/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204

        # Verify user is deleted
        get_response = await async_client.get(
            f"/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert get_response.status_code == 404

    async def test_delete_user_as_non_admin(
        self, async_client: AsyncClient, test_admin: User, user_token: str
    ):
        """Test deleting user as non-admin (should fail)."""
        response = await async_client.delete(
            f"/admin/users/{test_admin.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    async def test_delete_user_not_found(
        self, async_client: AsyncClient, admin_token: str
    ):
        """Test deleting nonexistent user."""
        response = await async_client.delete(
            "/admin/users/9999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404

    async def test_create_duplicate_username(
        self, async_client: AsyncClient, test_user: User, admin_token: str
    ):
        """Test creating user with duplicate username."""
        response = await async_client.post(
            "/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "username": "testuser",  # Already exists
                "email": "different@example.com",
                "password": "password123",
                "is_admin": False,
            },
        )

        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]
