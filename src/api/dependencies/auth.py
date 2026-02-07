import fastapi
import fastapi.security
import jwt

import config
from models.user import User


class Auth():
	OAUTH2_SCHEME = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/auth/token")

	def __init__(self) -> None:
		pass

	async def get_current_user(self, request: fastapi.Request | None = None) -> User | None:
		try:
			user = await self.get_current_user_with_exception(request)
		except fastapi.HTTPException:
			return None
		else:
			return user

	async def get_current_user_with_exception(self, request: fastapi.Request | None = None) -> User:
		if request is None:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

		token = request.cookies.get("Authorization-Token")

		if token is None or not token:
			token = await self.OAUTH2_SCHEME(request)

		try:
			payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Token expired")
		except jwt.InvalidTokenError:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

		user = await User.get(payload["sub"], fetch_links=True)

		if user is None:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="User not found")

		return user

	async def __call__(self, request: fastapi.Request) -> User:
		return await self.get_current_user_with_exception(request)


auth = Auth()
