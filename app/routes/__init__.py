from .auth_routes import router as auth_routes
from .crop_routes import router as crop_routes
from .farm_routes import router as farm_routes

__all__ = ["auth_routes", "crop_routes", "farm_routes"]
