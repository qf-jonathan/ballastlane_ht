"""Tests for user service."""
import pytest
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.mark.unit
class TestUserService:
    """Test user service."""

    async def test_create_user_success(self):
        """Test successful user creation."""
        user_data = UserCreate(
            username="newuser",
            email="newuser@example.com",
            password="password123",
            is_admin=False,
        )
        user = await UserService.create_user(user_data)

        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.is_active is True
        assert user.is_admin is False

    async def test_create_user_duplicate_username(self, test_user: User):
        """Test creating user with duplicate username."""
        user_data = UserCreate(
            username="testuser",  # Already exists
            email="different@example.com",
            password="password123",
            is_admin=False,
        )

        with pytest.raises(HTTPException) as exc:
            await UserService.create_user(user_data)
        assert exc.value.status_code == 400
        assert "Username already registered" in str(exc.value.detail)

    async def test_create_user_duplicate_email(self, test_user: User):
        """Test creating user with duplicate email."""
        user_data = UserCreate(
            username="differentuser",
            email="test@example.com",  # Already exists
            password="password123",
            is_admin=False,
        )

        with pytest.raises(HTTPException) as exc:
            await UserService.create_user(user_data)
        assert exc.value.status_code == 400
        assert "Email already registered" in str(exc.value.detail)

    async def test_get_user_by_id_success(self, test_user: User):
        """Test getting user by ID."""
        user = await UserService.get_user_by_id(test_user.id)
        assert user is not None
        assert user.id == test_user.id
        assert user.username == test_user.username

    async def test_get_user_by_id_not_found(self):
        """Test getting nonexistent user by ID."""
        with pytest.raises(HTTPException) as exc:
            await UserService.get_user_by_id(9999)
        assert exc.value.status_code == 404
        assert "User not found" in str(exc.value.detail)

    async def test_get_user_by_username_success(self, test_user: User):
        """Test getting user by username."""
        user = await UserService.get_user_by_username("testuser")
        assert user is not None
        assert user.username == "testuser"

    async def test_get_user_by_username_not_found(self):
        """Test getting nonexistent user by username."""
        with pytest.raises(HTTPException) as exc:
            await UserService.get_user_by_username("nonexistent")
        assert exc.value.status_code == 404

    async def test_get_all_users(self, test_user: User, test_admin: User):
        """Test getting all users."""
        users = await UserService.get_all_users()
        assert len(users) >= 2
        usernames = [u.username for u in users]
        assert "testuser" in usernames
        assert "admin" in usernames

    async def test_get_all_users_pagination(self, test_user: User, test_admin: User):
        """Test getting users with pagination."""
        users = await UserService.get_all_users(skip=0, limit=1)
        assert len(users) == 1

    async def test_update_user_username(self, test_user: User):
        """Test updating user username."""
        update_data = UserUpdate(username="updateduser")
        updated_user = await UserService.update_user(test_user.id, update_data)

        assert updated_user.username == "updateduser"
        assert updated_user.email == test_user.email

    async def test_update_user_email(self, test_user: User):
        """Test updating user email."""
        update_data = UserUpdate(email="updated@example.com")
        updated_user = await UserService.update_user(test_user.id, update_data)

        assert updated_user.email == "updated@example.com"
        assert updated_user.username == test_user.username

    async def test_update_user_password(self, test_user: User):
        """Test updating user password."""
        update_data = UserUpdate(password="newpassword123")
        updated_user = await UserService.update_user(test_user.id, update_data)

        # Verify password was changed (hash should be different)
        assert updated_user.hashed_password != test_user.hashed_password

    async def test_update_user_is_active(self, test_user: User):
        """Test updating user active status."""
        update_data = UserUpdate(is_active=False)
        updated_user = await UserService.update_user(test_user.id, update_data)

        assert updated_user.is_active is False

    async def test_update_user_is_admin(self, test_user: User):
        """Test updating user admin status."""
        update_data = UserUpdate(is_admin=True)
        updated_user = await UserService.update_user(test_user.id, update_data)

        assert updated_user.is_admin is True

    async def test_update_user_duplicate_username(self, test_user: User, test_admin: User):
        """Test updating to existing username."""
        update_data = UserUpdate(username="admin")  # Already exists

        with pytest.raises(HTTPException) as exc:
            await UserService.update_user(test_user.id, update_data)
        assert exc.value.status_code == 400
        assert "Username already taken" in str(exc.value.detail)

    async def test_update_user_duplicate_email(self, test_user: User, test_admin: User):
        """Test updating to existing email."""
        update_data = UserUpdate(email="admin@example.com")  # Already exists

        with pytest.raises(HTTPException) as exc:
            await UserService.update_user(test_user.id, update_data)
        assert exc.value.status_code == 400
        assert "Email already taken" in str(exc.value.detail)

    async def test_delete_user_success(self, test_user: User):
        """Test successful user deletion."""
        await UserService.delete_user(test_user.id)

        # Verify user is deleted
        user = await User.filter(id=test_user.id).first()
        assert user is None

    async def test_delete_user_not_found(self):
        """Test deleting nonexistent user."""
        with pytest.raises(HTTPException) as exc:
            await UserService.delete_user(9999)
        assert exc.value.status_code == 404
