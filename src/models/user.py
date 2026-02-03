import datetime

from pydantic import Field
import pymongo
from beanie import Document, Link
from pymongo import IndexModel

from .product import Product


class User(Document):
	username: str
	email: str
	first_name: str
	last_name: str | None = None
	role: str = "customer"
	password_hash: str
	phone_number: str
	cart: list[Link[Product]]
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))

	class Settings:
		name = "users"
		use_state_management = True
		indexes = [
			IndexModel([("username", pymongo.ASCENDING)], unique=True),
			IndexModel([("email", pymongo.ASCENDING)], unique=True),
		]
