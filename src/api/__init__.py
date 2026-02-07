import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = ("api_router", "templates_router", "AuthMiddleware")


from .middleware import AuthMiddleware
from .routes import api_router, templates_router
