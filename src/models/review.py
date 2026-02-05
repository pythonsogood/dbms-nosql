import datetime
from typing import Annotated

from annotated_types import Interval
from beanie import Document, Link
from pydantic import Field

from models import Product, User


class Review(Document):
	user: Link[User]
	product: Link[Product]
	rating: Annotated[int, Interval(ge=1, le=5)]
	comment: str
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))

	class Settings:
		name = "reviews"
		use_state_management = True
