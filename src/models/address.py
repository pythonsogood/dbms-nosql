from beanie import Document, Link
import pymongo
from pymongo import IndexModel

from .user import User


class Address(Document):
	user: Link[User]
	country: str
	city: str
	address: str
	zip_code: str

	class Settings:
		name = "addresses"
		use_state_management = True
		indexes = [
			IndexModel([("user", pymongo.ASCENDING)]),
			IndexModel([("user", pymongo.ASCENDING), ("address", pymongo.ASCENDING)]),
		]
