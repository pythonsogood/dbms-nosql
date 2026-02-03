import datetime

from beanie import Document, Link

from .user import User


class Order(Document):
	user: Link[User]
	created_at: datetime.datetime

	class Settings:
		name = "orders"
		use_state_management = True
