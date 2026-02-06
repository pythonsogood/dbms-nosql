from typing import Annotated

import fastapi
from beanie import PydanticObjectId
from beanie.operators import In

from api.dependencies import auth
from models import Product, ProductCategory, User

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
async def get_products(
	category_filter: Annotated[list[str], fastapi.Query(default_factory=list)],
	min_price: Annotated[float | None, fastapi.Query()] = None,
	max_price: Annotated[float | None, fastapi.Query()] = None
):
	query = Product.find_all()

	if category_filter:
		query = query.find(In(Product.category.name, category_filter))

	if min_price is not None:
		query = query.find(Product.price >= min_price)

	if max_price is not None:
		query = query.find(Product.price <= max_price)

	products = await query.to_list()

	return {"status": "success", "data": products}

@router.get("/product/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def get_product(product_id: Annotated[str, fastapi.Path()]):
	product = await Product.get(PydanticObjectId(product_id))

	if product is None:
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Product not found")

	return {"status": "success", "data": product}

@router.post("/product/{product_id}/stock", response_class=fastapi.responses.ORJSONResponse)
async def update_stock(
	product_id: str,
	change:  Annotated[int, fastapi.Body(embed=True)]
):
	product = await Product.get(PydanticObjectId(product_id))
	if not product:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	try:
		await product.update({"$inc": {Product.stock: change}})
		updated_product = await Product.get(PydanticObjectId(product_id))
		return {"status": "success", "new_stock": updated_product.stock}
	except Exception as e:
		raise fastapi.HTTPException(status_code=500, detail=str(e))

@router.post("/product/{product_id}/review", response_class=fastapi.responses.ORJSONResponse)
async def add_review(
	product_id: str,
	review: Annotated[dict, fastapi.Body()]
):
	# Review using $push
	from models import Review

	product = await Product.get(PydanticObjectId(product_id))
	if not product:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	new_review = Review(
		username=review.get("username", "Anonymous"),
		rating=review.get("rating", 5),
		comment=review.get("comment", "")
	)

	await product.update({"$push": {Product.reviews: new_review}})

	return {"status": "success", "message": "Review added"}

@router.post("/cart/remove", response_class=fastapi.responses.ORJSONResponse)
async def remove_from_cart(
	product_id: Annotated[str, fastapi.Body(embed=True)],
	user: Annotated[User, fastapi.Depends(auth)]
):

	from beanie import PydanticObjectId
	pid = PydanticObjectId(product_id)


	await user.update({"$pull": {"cart": {"$id": PydanticObjectId(product_id)}}})
	return {"status": "success", "message": "Item removed"}
