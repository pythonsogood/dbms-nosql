import datetime
import enum

from beanie import DecimalAnnotation, Document, Link
from pydantic import BaseModel, Field, NonNegativeInt

from models.product import Product

from .user import User


class OrderStatus(enum.Enum):
	PENDING = "pending"
	PAID = "paid"
	DELIVERED = "delivered"
	CANCELLED = "cancelled"


class OrderItem(BaseModel):
	product: Link[Product]
	quantity: NonNegativeInt


class Order(Document):
	user: Link[User]
	items: list[OrderItem] = Field(default_factory=list)
	status: OrderStatus = OrderStatus.PENDING
	total_price: DecimalAnnotation | None = None
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))

	class Settings:
		name = "orders"
		use_state_management = True
