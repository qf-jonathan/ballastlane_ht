"""Quick demo script to show the shell capabilities."""
import asyncio
from app.core.database import init_db, close_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.security import get_password_hash


async def demo():
    """Run a quick demo."""
    await init_db()

    print("🚀 Shell Demo - Testing Interactive Capabilities\n")

    # 1. Query users
    print("1️⃣  Getting all users:")
    users = await User.all()
    for user in users:
        print(f"   • {user.username} ({user.email}) - Admin: {user.is_admin}")

    # 2. Filter query
    print("\n2️⃣  Finding admin users:")
    admins = await User.filter(is_admin=True)
    print(f"   Found {len(admins)} admin(s)")

    # 3. Authentication
    print("\n3️⃣  Testing authentication:")
    try:
        token = await AuthService.login("admin", "admin123")
        print(f"   ✓ Login successful")
        print(f"   Token: {token.access_token[:50]}...")

        # Verify token
        user = await AuthService.get_current_user(token.access_token)
        print(f"   ✓ Verified as: {user.username}")
    except Exception as e:
        print(f"   ✗ Login failed: {e}")

    # 4. Create test user
    print("\n4️⃣  Creating a test user:")
    test_user = await User.create(
        username="shelltest",
        email="shelltest@example.com",
        hashed_password=get_password_hash("test123"),
        is_active=True,
        is_admin=False
    )
    print(f"   ✓ Created: {test_user.username} (ID: {test_user.id})")

    # 5. Update user
    print("\n5️⃣  Updating user:")
    test_user.email = "updated@example.com"
    await test_user.save()
    print(f"   ✓ Updated email to: {test_user.email}")

    # 6. Count users
    print("\n6️⃣  Counting users:")
    total = await User.all().count()
    print(f"   Total users in database: {total}")

    # 7. Clean up
    print("\n7️⃣  Cleaning up test user:")
    await test_user.delete()
    print(f"   ✓ Deleted test user")

    await close_db()
    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    asyncio.run(demo())
