import datetime

from beanie import DecimalAnnotation, Document, Link

from .product_category import ProductCategory


class Product(Document):
	name: str
	description: str | None = None
	category: Link[ProductCategory]
	price: DecimalAnnotation
	created_at: datetime.datetime

	class Settings:
		name = "products"
		use_state_management = True
