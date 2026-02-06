from typing import Annotated

import fastapi
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from api.dependencies import auth
from models import User

router = fastapi.APIRouter(prefix="/auth")


class RegisterRequest(BaseModel):
	username: str
	email: EmailStr
	first_name: str
	last_name: str | None = None
	phone_number: str | None = None
	password: str


class LoginRequest(BaseModel):
	username: str
	password: str


class ChangePasswordRequest(BaseModel):
	password: str
	new_password: str


class ChangePhoneRequest(BaseModel):
	password: str
	phone_number: str


class ChangeNameRequest(BaseModel):
	first_name: str | None = None
	last_name: str | None = None


@router.post("/register", response_class=fastapi.responses.ORJSONResponse)
async def register(register_request: RegisterRequest):
	user = User(
		username=register_request.username,
		email=register_request.email,
		first_name=register_request.first_name,
		last_name=register_request.last_name,
		password_hash=User.hash_password(register_request.password),
		phone_number=register_request.phone_number
	)

	await user.save()

	return {"status": "success", "data": user.create_jwt_token()}

@router.post("/login", response_class=fastapi.responses.ORJSONResponse)
async def login(login_request: LoginRequest):
	user = await User.find_one({"username": login_request.username})

	if user is None or not user.verify_password(login_request.password):
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	return {"status": "success", "data": user.create_jwt_token()}

@router.post("/token", response_class=fastapi.responses.ORJSONResponse)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()]):
	user = await User.find_one({"username": form_data.username})

	if user is None or not user.verify_password(form_data.password):
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	return {"access_token": user.create_jwt_token(), "token_type": "bearer"}

@router.get("/whoami", response_class=fastapi.responses.ORJSONResponse)
async def whoami(user: Annotated[User, fastapi.Depends(auth)]):
	return {"status": "success", "data": f"Hello, {user.username}"}

@router.post("/change_password", response_class=fastapi.responses.ORJSONResponse)
async def change_password(user: Annotated[User, fastapi.Depends(auth)], change_password_request: ChangePasswordRequest):
	if not user.verify_password(change_password_request.password):
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	user.password_hash = User.hash_password(change_password_request.new_password)

	await user.save()

	return {"status": "success", "data": "Password changed"}

@router.post("/change_phone_number", response_class=fastapi.responses.ORJSONResponse)
async def change_phone_number(user: Annotated[User, fastapi.Depends(auth)], change_phone_number_request: ChangePhoneRequest):
	if not user.verify_password(change_phone_number_request.password):
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	user.phone_number = change_phone_number_request.phone_number

	await user.save()

	return {"status": "success", "data": "Phone number changed"}

@router.post("/change_name", response_class=fastapi.responses.ORJSONResponse)
async def change_name(user: Annotated[User, fastapi.Depends(auth)], change_name: ChangeNameRequest):
	if change_name.first_name is None and change_name.last_name is None:
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="At least one name must be provided")

	if change_name.first_name is not None:
		user.first_name = change_name.first_name

	if change_name.last_name is not None:
		user.last_name = change_name.last_name

	await user.save()

	return {"status": "success", "data": "Name changed"}
