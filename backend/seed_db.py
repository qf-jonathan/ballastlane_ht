"""Script to seed database with initial admin user."""
import asyncio

from app.core.database import init_db, close_db
from app.core.security import get_password_hash
from app.models.user import User


async def seed_admin_user():
    """Create an initial admin user."""
    await init_db()

    # Check if admin already exists
    admin_exists = await User.filter(username="admin").first()

    if not admin_exists:
        admin = await User.create(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True,
        )
        print(f"✓ Admin user created: {admin.username}")
    else:
        print("✓ Admin user already exists")

    # Create a regular test user
    test_user_exists = await User.filter(username="testuser").first()

    if not test_user_exists:
        test_user = await User.create(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("test1234"),
            is_admin=False,
            is_active=True,
        )
        print(f"✓ Test user created: {test_user.username}")
    else:
        print("✓ Test user already exists")

    await close_db()


if __name__ == "__main__":
    print("Seeding database...")
    asyncio.run(seed_admin_user())
    print("Database seeded successfully!")
