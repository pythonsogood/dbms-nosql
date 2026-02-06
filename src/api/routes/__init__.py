import os
import sys

sys.path.append(os.path.abspath("../.."))


__all__ = ("api_router", "templates_router")


from fastapi import APIRouter

from .auth import router as auth_router
from .shop import router as shop_router
from .templates import router as _templates_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(shop_router)

templates_router = APIRouter()

templates_router.include_router(_templates_router)