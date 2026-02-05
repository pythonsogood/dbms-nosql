from typing import Annotated
import fastapi
from pydantic import BaseModel

from api.dependencies import auth
from models.user import User

router = fastapi.APIRouter(prefix="/auth")


class LoginRequest(BaseModel):
	username: str
	password: str


@router.post("/login")
async def login(login_request: LoginRequest):
	user = await User.find_one({"username": login_request.username})

	if user is None or not user.verify_password(login_request.password):
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	return {"status": "success", "data": user.create_jwt_token()}

@router.get("/whoami")
async def whoami(user: Annotated[User, fastapi.Depends(auth)]):
	return {"status": "success", "data": f"Hello, {user.username}"}
