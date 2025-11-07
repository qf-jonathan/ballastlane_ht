"""Pytest fixtures and configuration."""
import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise

from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from main import app


@pytest.fixture(scope="function", autouse=True)
async def initialize_tests():
    """Initialize test database for each test."""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.user"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture
async def test_user() -> User:
    """Create a test user."""
    user = await User.create(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        is_active=True,
        is_admin=False,
    )
    return user


@pytest.fixture
async def test_admin() -> User:
    """Create a test admin user."""
    admin = await User.create(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_admin=True,
    )
    return admin


@pytest.fixture
async def inactive_user() -> User:
    """Create an inactive test user."""
    user = await User.create(
        username="inactive",
        email="inactive@example.com",
        hashed_password=get_password_hash("inactive123"),
        is_active=False,
        is_admin=False,
    )
    return user


@pytest.fixture
def user_token(test_user: User) -> str:
    """Create a JWT token for test user."""
    return create_access_token(data={"sub": test_user.username})


@pytest.fixture
def admin_token(test_admin: User) -> str:
    """Create a JWT token for admin user."""
    return create_access_token(data={"sub": test_admin.username})


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
