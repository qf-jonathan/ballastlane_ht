from tortoise import Tortoise

from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models.user", "app.models.pokemon", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    """Initialize database connection."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user", "app.models.pokemon"]},
    )
    await Tortoise.generate_schemas()


async def close_db():
    """Close database connection."""
    await Tortoise.close_connections()
