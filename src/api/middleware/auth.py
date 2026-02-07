from collections.abc import Awaitable, Callable

import fastapi

from api.dependencies import auth


class AuthMiddleware:
	async def __call__(self, request: fastapi.Request, call_next: Callable[[fastapi.Request], Awaitable[fastapi.Response]]) -> fastapi.Response:
		user = await auth.get_current_user(request)

		request.scope["user"] = user

		if user is not None:
			request.scope["user_cart"] = await user.fetch_cart()
		else:
			request.scope["user_cart"] = []

		response = await call_next(request)

		return response
