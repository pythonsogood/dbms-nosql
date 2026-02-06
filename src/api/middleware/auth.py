from collections.abc import Awaitable, Callable
from typing import Annotated

import fastapi

from api.dependencies import auth
from models import User


class AuthMiddleware:
	async def __call__(self, request: fastapi.Request, user: Annotated[User, fastapi.Depends(auth)], call_next: Callable[[fastapi.Request], Awaitable[fastapi.Response]]) -> fastapi.Response:
		request.scope["user"] = user

		response = await call_next(request)

		return response
