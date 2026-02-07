import asyncio
import os
from contextlib import asynccontextmanager
from decimal import Decimal

import fastapi
import uvicorn
from beanie import init_beanie
from fastapi.staticfiles import StaticFiles
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

import config
from api import AuthMiddleware, api_router, dependencies, templates_router
from api.dependencies import templates as get_templates
from models import Address, Order, Product, ProductCategory, ProductGender, User, Review

templates = get_templates()

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
	mongo = dependencies.database()

	document_models = [User, Address, ProductCategory, Product, Order, Review]

	await init_beanie(database=mongo[config.MONGODB_DATABASE], document_models=document_models, allow_index_dropping=True)

# 	categories = {category.name: category for category in await ProductCategory.find_all().to_list()}

# 	await Product(
# 		name="COOFANDY Mens T-Shirts 100% Cotton Crewneck Short Sleeve Tees Casual Plain Shirts",
# 		description="""100% PURE COTTON: This mens t shirt is made from midweight 100% organic cotton fabric. Skin friendly and so breathable this cotton shirt will bring you a more relaxed and comfortable wearing experience
# TIMELESS AND BELOVED LOOK: Coofandy cotton t shirt features a classic thickened ribbed crewneck design with double-needle topstitching around the shoulder, so it won't deform easily and will last longer as one of your favourite basics choices
# ALWAYS NEED A BASIC TEE: Every wardrobe needs a solid foundation. As your all-season collection, this crew t-shirt is perfect for everyday casual wear, streetwear, work shirt, gym shirt, athletic shirt, and as a versatile base layer under your coats, jackets and sweathshirts
# GREAT GIFT IDEAS: They're simple, built for comfort and durability, fit just right and are made for everyday style, making them perfect for giving as a gift to yourself, father, husband, friends or other loved ones. Don't miss out!
# WARM TIPS: Machine wash, hang to dry. Size is US size. Please refer to our SIZE CHART to help you choose""",
# 		category=categories["Shirts"],
# 		brand="COOFANDY",
# 		gender=ProductGender.MEN,
# 		sizes=["M", "L", "XL", "XXL"],
# 		stock=71,
# 		image_url="https://m.media-amazon.com/images/I/71V7fnZqODL._AC_SY550_.jpg",
# 		price=Decimal("16.99"),
# 	).save()

	yield

app = fastapi.FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware())

@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: fastapi.Request, exc: StarletteHTTPException):
	if request.url.path.startswith("/api"):
		return await http_exception_handler(request, exc)

	return templates.TemplateResponse(request=request, name="error.html", context={
		"detail": exc.detail,
		"status_code": exc.status_code,
	})

app.include_router(api_router, prefix="/api/v1")
app.include_router(templates_router)

def main() -> None:
	if os.name == "nt":
		asyncio.set_event_loop_policy(asyncio._WindowsSelectorEventLoopPolicy())

	uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)


if __name__ == "__main__":
	asyncio.run(main())
