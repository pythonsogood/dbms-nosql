from beanie import Document, Link


class ProductCategory(Document):
	name: str
	parent: Link["ProductCategory"] | None = None

	class Settings:
		name = "product_categories"
		use_state_management = True
