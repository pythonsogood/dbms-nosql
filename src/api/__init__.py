import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = ("api_router", "templates_router")


from .routes import api_router, templates_router
