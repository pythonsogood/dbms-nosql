from typing import Annotated

import fastapi
from annotated_types import Interval
from beanie import PydanticObjectId
from beanie.operators import In
from pydantic import BaseModel

from api.dependencies import auth
from models import Product, ProductCategory, User, Review

router = fastapi.APIRouter(prefix="/shop")


class PostReviewRequest(BaseModel):
	rating: Annotated[int, Interval(ge=1, le=5)]
	comment: str


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
	if min_price is not None and max_price is not None and min_price > max_price:
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="Invalid price range")

	query = Product.find_all()

	if category_filter:
		query = query.find(In(Product.category.name, category_filter))  # pyright: ignore[reportAttributeAccessIssue]

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

@router.post("/product/{product_id}/review", response_class=fastapi.responses.ORJSONResponse)
async def add_review(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Path()], review: PostReviewRequest):
	product = await Product.get(PydanticObjectId(product_id))

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	product_review = Review(user=user, product=product, rating=review.rating, comment=review.comment)

	await product_review.save()

	return {"status": "success", "message": "Review added"}

@router.patch("/product/{product_id}/{review_id}/review", response_class=fastapi.responses.ORJSONResponse)
async def edit_review(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Path()], review_id: Annotated[str, fastapi.Path()], review: PostReviewRequest):
	product = await Product.get(PydanticObjectId(product_id))

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	product_review = Review(user=user, product=product, rating=review.rating, comment=review.comment)

	await product_review.save()

	return {"status": "success", "message": "Review added"}

@router.put("/cart/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def add_to_cart(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Body(embed=True)]):
	product = await Product.get(product_id)

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	user.cart.append(product)

	await user.save()

	return {"status": "success", "message": "Product added to cart"}

@router.delete("/cart/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def remove_from_cart(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Body(embed=True)]):
	product = await Product.get(product_id)

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	if product not in user.cart:
		raise fastapi.HTTPException(status_code=404, detail="Product not found in cart")

	user.cart.remove(product)

	return {"status": "success", "message": "Product removed from removed"}
