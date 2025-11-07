#!/usr/bin/env python
"""
Interactive IPython shell with pre-loaded models and utilities.
Similar to Django's shell - all models and utilities are available.

Usage:
    python shell.py
    python shell.py --sql  # Enable SQL query logging
"""
import argparse
import asyncio
import logging
import sys

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
from tortoise import Tortoise

# Import all models
from app.models.user import User

# Import services
from app.services.auth_service import AuthService
from app.services.user_service import UserService

# Import schemas
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
)

# Import security utilities
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

# Import config
from app.core.config import settings


async def init_db():
    """Initialize database connection."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user"]},
    )
    print("✓ Database initialized")


def print_banner():
    """Print welcome banner with available objects."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║             Pokedex API - Interactive Shell                  ║
╚══════════════════════════════════════════════════════════════╝

📦 Available Models:
   • User

🔧 Available Services:
   • AuthService
   • UserService

📋 Available Schemas:
   • UserCreate, UserUpdate, UserResponse
   • UserLogin, Token

🔐 Security Utilities:
   • create_access_token(data: dict) -> str
   • decode_access_token(token: str) -> dict
   • get_password_hash(password: str) -> str
   • verify_password(plain: str, hashed: str) -> bool

⚙️  Settings:
   • settings (application configuration)

🔄 Async Helper:
   • run(coroutine) - Execute async functions easily

🐢 SQL Logging:
   • enable_sql_logging() - Show SQL queries
   • enable_sql_logging(verbose=True) - Show detailed SQL queries
   • disable_sql_logging() - Hide SQL queries

💡 Quick Examples:
   # Get all users (using the 'run' helper)
   users = run(User.all())
   print(users)

   # Get specific user
   user = run(User.filter(username="admin").first())

   # Create a new user
   user = run(User.create(
       username="newuser",
       email="new@example.com",
       hashed_password=get_password_hash("password"),
       is_active=True,
       is_admin=False
   ))

   # Login user
   token = run(AuthService.login("admin", "admin123"))

   # Get current user from token
   user = run(AuthService.get_current_user(token.access_token))

   # Use UserService
   users = run(UserService.get_all_users())

   # The 'loop' object is available for async operations
   # Use loop.run_until_complete(your_async_function())

Type 'exit' or Ctrl-D to quit.
═══════════════════════════════════════════════════════════════
"""
    print(banner)


def main():
    """Entry point for shell command."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Interactive shell with SQL logging support")
    parser.add_argument(
        "--sql",
        action="store_true",
        help="Enable SQL query logging to see all executed queries"
    )
    parser.add_argument(
        "--sql-debug",
        action="store_true",
        help="Enable verbose SQL logging with query parameters"
    )
    args = parser.parse_args()

    # Configure SQL logging if requested
    if args.sql or args.sql_debug:
        logging.basicConfig(level=logging.DEBUG if args.sql_debug else logging.INFO)
        logger = logging.getLogger("tortoise")
        logger.setLevel(logging.DEBUG)

        # Create console handler with custom format
        handler = logging.StreamHandler()
        if args.sql_debug:
            formatter = logging.Formatter(
                '\n🐢 %(levelname)s - %(name)s\n%(message)s\n'
            )
        else:
            formatter = logging.Formatter(
                '🐢 SQL: %(message)s'
            )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        print("✓ SQL logging enabled\n")

    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Initialize database synchronously
    loop.run_until_complete(init_db())

    # Print banner
    print_banner()

    # Helper function for running async code
    def run(coro):
        """Helper to run async functions. Usage: run(User.all())"""
        return loop.run_until_complete(coro)

    # SQL logging toggle functions
    def enable_sql_logging(verbose=False):
        """Enable SQL query logging."""
        logger = logging.getLogger("tortoise")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            if verbose:
                formatter = logging.Formatter(
                    '\n🐢 %(levelname)s - %(name)s\n%(message)s\n'
                )
            else:
                formatter = logging.Formatter('🐢 SQL: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        print("✓ SQL logging enabled")

    def disable_sql_logging():
        """Disable SQL query logging."""
        logger = logging.getLogger("tortoise")
        logger.setLevel(logging.WARNING)
        logger.handlers.clear()
        print("✓ SQL logging disabled")

    # Populate namespace with useful objects
    namespace = {
        # Models
        "User": User,

        # Services
        "AuthService": AuthService,
        "UserService": UserService,

        # Schemas
        "UserCreate": UserCreate,
        "UserUpdate": UserUpdate,
        "UserResponse": UserResponse,
        "UserLogin": UserLogin,
        "Token": Token,

        # Security utilities
        "create_access_token": create_access_token,
        "decode_access_token": decode_access_token,
        "get_password_hash": get_password_hash,
        "verify_password": verify_password,

        # Config
        "settings": settings,

        # Tortoise utilities
        "Tortoise": Tortoise,

        # Event loop and helpers
        "loop": loop,
        "run": run,
        "enable_sql_logging": enable_sql_logging,
        "disable_sql_logging": disable_sql_logging,
    }

    # Start IPython with the existing event loop
    try:
        from IPython import start_ipython
        start_ipython(
            argv=[],
            user_ns=namespace,
        )
    except (EOFError, KeyboardInterrupt):
        print("\n\n✓ Shell closed")
    finally:
        # Cleanup
        loop.run_until_complete(Tortoise.close_connections())
        print("\n✓ Database connections closed")


if __name__ == "__main__":
    main()
