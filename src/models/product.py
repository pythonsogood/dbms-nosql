import datetime
import enum
from typing import TYPE_CHECKING

from beanie import BackLink, DecimalAnnotation, Document, Link
from pydantic import Field, NonNegativeInt

from .product_category import ProductCategory

if TYPE_CHECKING:
	from models.review import Review


class ProductGender(enum.Enum):
	MEN = "men"
	WOMEN = "women"
	UNISEX = "unisex"


class Product(Document):
	name: str
	description: str | None = None
	category: Link[ProductCategory]
	brand: str | None = None
	gender: ProductGender = ProductGender.UNISEX
	sizes: list[str] = Field(default_factory=list)
	stock: NonNegativeInt = 0
	price: DecimalAnnotation
	image_url: str = "https://media.istockphoto.com/id/1396160859/photo/baby-and-child-clothes-toys-in-box-second-hand-apparel-idea-circular-fashion-donation-charity.webp?b=1&s=612x612&w=0&k=20&c=uSweFaKbnO2xPEiPLj-lcoUKttjJfVfKMNPOhaueWEE="
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))
	reviews: list[BackLink["Review"]] = Field(json_schema_extra={"original_field": "product"})

	class Settings:
		name = "products"
		use_state_management = True
