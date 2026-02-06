import datetime
import enum

from beanie import DecimalAnnotation, Document, Link
from pydantic import BaseModel, Field, NonNegativeInt

from .product_category import ProductCategory
from .review import Review


class ProductGender(enum.Enum):
	MEN = "men"
	WOMEN = "women"
	UNISEX = "unisex"


class ProductVariant(BaseModel):
	size: str
	color: str
	sku: str
	stock: NonNegativeInt = 0


class Product(Document):
	name: str
	description: str | None = None
	category: Link[ProductCategory]
	brand: str | None = None
	gender: ProductGender = ProductGender.UNISEX
	variants: list[ProductVariant] = Field(default_factory=list)
	reviews: list[Review] = Field(default_factory=list)

	class Settings:
		name = "products"
		use_state_management = True
