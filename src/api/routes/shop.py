from typing import Annotated

import fastapi
from beanie import PydanticObjectId
from beanie.operators import In

from models import Product, ProductCategory

router = fastapi.APIRouter(prefix="/shop")


@router.get("/product_categories", response_class=fastapi.responses.ORJSONResponse)
async def get_product_categories():
	categories = await ProductCategory.find_all().to_list()

	return {"status": "success", "data": categories}

@router.get("/product_brands", response_class=fastapi.responses.ORJSONResponse)
async def get_product_brands():
	categories = await Product.distinct("brands")

	return {"status": "success", "data": categories}

@router.get("/products", response_class=fastapi.responses.ORJSONResponse)
async def get_products(category_filter: Annotated[list[str], fastapi.Query(default_factory=list)]):
	products_query = Product.find_all()

	if category_filter:
		products_query = Product.find_many(In(Product.category.name, category_filter))  # pyright: ignore[reportAttributeAccessIssue]

	products = await products_query.to_list()

	return {"status": "success", "data": products}

@router.get("/product/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def get_product(product_id: Annotated[str, fastapi.Path()]):
	product = await Product.get(PydanticObjectId(product_id))

	if product is None:
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Product not found")

	return {"status": "success", "data": product}
