"""Demo script to show SQL logging."""
import asyncio
import logging
from app.core.database import init_db, close_db
from app.models.user import User


async def demo():
    """Run SQL logging demo."""
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("tortoise")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('🐢 SQL: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    await init_db()

    print("\n" + "="*60)
    print("SQL Logging Demo")
    print("="*60 + "\n")

    print("1️⃣  Fetching all users:\n")
    users = await User.all()
    print(f"   → Found {len(users)} users\n")

    print("\n2️⃣  Filtering admin users:\n")
    admins = await User.filter(is_admin=True)
    print(f"   → Found {len(admins)} admin(s)\n")

    print("\n3️⃣  Getting specific user by username:\n")
    admin = await User.filter(username="admin").first()
    print(f"   → Found: {admin.username if admin else 'None'}\n")

    print("\n4️⃣  Count query:\n")
    count = await User.all().count()
    print(f"   → Total users: {count}\n")

    print("\n5️⃣  Ordering results:\n")
    recent = await User.all().order_by("-created_at").limit(2)
    print(f"   → Got {len(recent)} most recent users\n")

    await close_db()
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(demo())
