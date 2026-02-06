from typing import Annotated

import fastapi
from beanie.operators import In

from models import Product, ProductCategory

router = fastapi.APIRouter(prefix="/shop")


@router.get("/product_categories", response_class=fastapi.responses.ORJSONResponse)
async def get_product_categories():
	categories = await ProductCategory.find_all().to_list()

	return {"status": "success", "data": categories}

@router.get("/products", response_class=fastapi.responses.ORJSONResponse)
async def get_products(category_filter: Annotated[list[str], fastapi.Query(default_factory=list)]):
	products_query = Product.find_all()

	if category_filter:
		products_query = Product.find_many(In(Product.category.name, category_filter))

	products = await products_query.to_list()

	return {"status": "success", "data": products}
