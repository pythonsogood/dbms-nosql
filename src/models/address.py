from beanie import Document, Link

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
