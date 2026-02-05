import datetime
import os

from dotenv import load_dotenv


load_dotenv()

MONGODB_CONNECTION: str = os.getenv("MONGODB_CONNECTION")
MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE")

JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

assert MONGODB_CONNECTION is not None, "MONGODB_CONNECTION is not set"
assert MONGODB_DATABASE is not None, "MONGODB_DATABASE is not set"

assert JWT_SECRET_KEY is not None, "JWT_SECRET_KEY is not set"

PORT: int = int(os.getenv("PORT", 8000))

JWT_TOKEN_EXPIRATION: datetime.timedelta = datetime.timedelta(seconds=float(os.getenv("JWT_TOKEN_EXPIRATION", 72 * 60 * 60)))
