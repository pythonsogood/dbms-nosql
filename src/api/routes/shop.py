from typing import Annotated

import fastapi
from annotated_types import Interval
from beanie import PydanticObjectId
from beanie.operators import In
from pydantic import BaseModel, NonNegativeInt

from api.dependencies import auth
from models import Address, Order, Product, ProductCategory, Review, User, UserCart

router = fastapi.APIRouter(prefix="/shop")


class PostReviewRequest(BaseModel):
	rating: Annotated[int, Interval(ge=1, le=5)]
	comment: str


class AddAddressRequest(BaseModel):
	country: str
	city: str
	address: str
	zip_code: str


@router.get("/product_categories", response_class=fastapi.responses.ORJSONResponse)
async def get_product_categories():
	categories = await ProductCategory.find_many().to_list()

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

	query = Product.find_many(fetch_links=True)

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
	product = await Product.get(PydanticObjectId(product_id), fetch_links=True)

	if product is None:
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Product not found")

	return {"status": "success", "data": product}

@router.delete("/product/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def delete_product(product_id: Annotated[str, fastapi.Path()]):
	product = await Product.get(PydanticObjectId(product_id), fetch_links=True)

	if product is None:
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Product not found")

	await product.delete()

	return {"status": "success", "data": product}

@router.post("/product/{product_id}/review", response_class=fastapi.responses.ORJSONResponse)
async def add_review(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Path()], review: PostReviewRequest):
	product = await Product.get(PydanticObjectId(product_id))

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	product_review = Review(user=user, product=product, rating=review.rating, comment=review.comment)

	await product_review.save()

	return {"status": "success", "message": "Review added"}

@router.put("/cart/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def add_to_cart(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Path(embed=True)], size: Annotated[str, fastapi.Query()], quantity: Annotated[NonNegativeInt, fastapi.Query()] = 1):
	product = await Product.get(product_id)

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	update_result = await user.get_pymongo_collection().update_one({
		"_id": user.id,
		"cart.product_id": product.id,
		"cart.size": size,
	}, {
		"$inc": {"cart.$.quantity": quantity}
	})

	if update_result.matched_count == 0:
		await user.update({
			"$push": {
				"cart": UserCart(
					product_id=product.id,
					size=size,
					quantity=quantity,
				).model_dump()
			},
		})

	return {"status": "success", "message": "Product added to cart"}

@router.patch("/cart/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def add_to_cart_patch(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Path(embed=True)], size: Annotated[str, fastapi.Query()], quantity: Annotated[int, fastapi.Query()] = 1):
	product = await Product.get(product_id)

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	if quantity > 0:
		update_result = await user.get_pymongo_collection().update_one({
			"_id": user.id,
			"cart.product_id": product.id,
			"cart.size": size,
		}, {
			"$set": {"cart.$.quantity": quantity}
		})

		if update_result.matched_count == 0:
			await user.update({
				"$push": {
					"cart": UserCart(
						product_id=product.id,
						size=size,
						quantity=quantity,
					).model_dump(),
				},
			})
	else:
		await user.update({
			"$pull": {
				"cart": {
					"product_id": product.id,
					"size": size,
				},
			},
		})

	return {"status": "success", "message": "Product quantity changed in cart"}

@router.delete("/cart/{product_id}", response_class=fastapi.responses.ORJSONResponse)
async def remove_from_cart(user: Annotated[User, fastapi.Depends(auth)], product_id: Annotated[str, fastapi.Path(embed=True)], size: Annotated[str, fastapi.Query()]):
	product = await Product.get(product_id)

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	update_result = await user.get_pymongo_collection().update_one({
		"_id": user.id,
	}, {
		"$pull": {
			"cart": {
				"product_id": product.id,
				"size": size,
			},
		},
	})

	if update_result.modified_count == 0:
		raise fastapi.HTTPException(status_code=404, detail="Product not found in cart")

	return {"status": "success", "message": "Product removed from removed"}

@router.get("/addresses", response_class=fastapi.responses.ORJSONResponse)
async def get_addresses(user: Annotated[User, fastapi.Depends(auth)]):
	addresses = await Address.find_all().to_list()

	return {"status": "success", "data": addresses}

@router.put("/address", response_class=fastapi.responses.ORJSONResponse)
async def add_address(user: Annotated[User, fastapi.Depends(auth)], address: AddAddressRequest):
	new_address = Address(user=user, country=address.country, city=address.city, address=address.address, zip_code=address.zip_code)

	await new_address.save()

	return {"status": "success", "message": "Address added"}

@router.delete("/address/{address_id}", response_class=fastapi.responses.ORJSONResponse)
async def remove_addresses(user: Annotated[User, fastapi.Depends(auth)], address_id: Annotated[str, fastapi.Path(embed=True)]):
	address = await Address.get(address_id)

	if address is None:
		raise fastapi.HTTPException(status_code=404, detail="Address not found")

	await address.delete()

	return {"status": "success", "message": "Address removed"}

@router.delete("/admin_stats", response_class=fastapi.responses.ORJSONResponse)
async def admin_stats(user: Annotated[User, fastapi.Depends(auth)]):
	if user.role != "admin":
		raise fastapi.HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="Forbidden")

	order_stats = await Order.aggregate([
		{"$group": {
			"_id": None,
			"total_orders": {"$sum": 1},
			"total_revenue": {"$sum": "$total_price"},
		}},
	]).to_list()

	total_orders = order_stats[0]["total_orders"] if order_stats else 0
	total_revenue = order_stats[0]["total_revenue"] if order_stats else 0

	product_stats = await Product.aggregate([
		{"$group": {
			"_id": None,
			"total_stock": {"$sum": "$stock"},
		}},
	]).to_list()

	total_stock = product_stats[0]["total_stock"] if product_stats else 0

	products = await Product.find_many(fetch_links=True).to_list()

	return {
		"total_orders": total_orders,
		"total_revenue": total_revenue,
		"total_stock": total_stock,
		"products": products
	}
