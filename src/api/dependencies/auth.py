from typing import Annotated

import fastapi
import jwt

import config
from models.user import User


class Auth():
	def __init__(self) -> None:
		pass

	async def __call__(self, authorization: Annotated[str, fastapi.Header()]) -> User:
		scheme, _, token = authorization.partition(" ")

		if scheme.lower() != "bearer":
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

		try:
			payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Token expired")
		except jwt.InvalidTokenError:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

		user = await User.get(payload["sub"])

		if user is None:
			raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="User not found")

		return user


auth = Auth()
