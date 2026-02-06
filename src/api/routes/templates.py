import fastapi

from api.dependencies import templates as get_templates

from models import Product, ProductCategory

templates = get_templates()

router = fastapi.APIRouter()

@router.get("/", response_class=fastapi.responses.HTMLResponse)
async def index(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="index.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/login", response_class=fastapi.responses.HTMLResponse)
async def login(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="login.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/register", response_class=fastapi.responses.HTMLResponse)
async def register(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="register.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/logout", response_class=fastapi.responses.HTMLResponse)
async def logout(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="logout.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/shop", response_class=fastapi.responses.HTMLResponse)
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

@router.get("/admin", response_class=fastapi.responses.HTMLResponse)
async def admin(request: fastapi.Request):
	from models import Order, Product

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

@router.get("/cart", response_class=fastapi.responses.HTMLResponse)
async def cart(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="cart.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})

@router.get("/remove_from_cart", response_class=fastapi.responses.PlainTextResponse)
async def remove_from_cart(request: fastapi.Request):
	return "Not implemented yet"

@router.get("/product", response_class=fastapi.responses.HTMLResponse)
async def product(request: fastapi.Request):
	return templates.TemplateResponse(request=request, name="product.html", context={
		"get_flashed_messages": lambda *args, **kwargs: []
	})
