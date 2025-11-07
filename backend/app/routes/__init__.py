from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.pokemon import router as pokemon_router

__all__ = ["auth_router", "admin_router", "pokemon_router"]
