from typing import Annotated

import fastapi
from beanie import PydanticObjectId

from api.dependencies import templates as get_templates
from models import Order, Product, ProductCategory

templates = get_templates()

router = fastapi.APIRouter()

@router.get("/")
async def index(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="index.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/login")
async def login(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="login.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/register")
async def register(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="register.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/logout")
async def logout(request: fastapi.Request):
	response = fastapi.responses.RedirectResponse(url="/")
	response.delete_cookie("Authorization-Token")

	return response

@router.get("/shop")
async def shop(
	request: fastapi.Request,
	category: str | None = None,
	min_price: float | None = None,
	max_price: float | None = None
):
	query = Product.find_all()

	if category:
		query = query.find(Product.category.name == category)  # pyright: ignore[reportAttributeAccessIssue]

	if min_price is not None:
		query = query.find(Product.price >= min_price)
	if max_price is not None:
		query = query.find(Product.price <= max_price)

	products = await query.to_list()

	categories = await ProductCategory.find_all().to_list()

	return templates.TemplateResponse(request=request, name="shop.html", context={
		"get_flashed_messages": lambda *args, **kwargs: [],
		"products": products,
		"categories": categories,
		"current_category": category,
		"min_price": min_price,
		"max_price": max_price
	})

@router.get("/admin")
async def admin(request: fastapi.Request):
	pipeline = [
		{"$group": {"_id": None, "total_orders": {"$sum": 1}, "total_revenue": {"$sum": "$total_price"}}}
	]
	stats = await Order.aggregate(pipeline).to_list()

	total_orders = stats[0]["total_orders"] if stats else 0
	total_revenue = stats[0]["total_revenue"] if stats else 0

	products = await Product.find_all().to_list()

	return templates.TemplateResponse(request=request, name="admin.html", context={
		"get_flashed_messages": lambda *args, **kwargs: [],
		"total_orders": total_orders,
		"total_revenue": total_revenue,
		"products": products
	})

@router.get("/cart")
async def cart(request: fastapi.Request):
	if request.user is None:
		return fastapi.responses.RedirectResponse(url="/login")

	return templates.TemplateResponse(request=request, name="cart.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/product/{product_id}")
async def product(request: fastapi.Request, product_id: Annotated[str, fastapi.Path()]):
	product = await Product.get(PydanticObjectId(product_id), fetch_links=True)

	if product is None:
		raise fastapi.HTTPException(status_code=404, detail="Product not found")

	return templates.TemplateResponse(request=request, name="product.html", context={
		"get_flashed_messages": lambda *args, **kwargs: [],
		"product": product,
	})
