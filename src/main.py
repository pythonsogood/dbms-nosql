import asyncio
from decimal import Decimal
import os
from contextlib import asynccontextmanager

import fastapi
import uvicorn
from beanie import init_beanie
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

import config
from api import AuthMiddleware, api_router, dependencies, templates_router
from models import Address, Order, Product, ProductCategory, ProductGender, User, Review


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
	mongo = dependencies.database()

	document_models = [User, Address, ProductCategory, Product, Order, Review]

	await init_beanie(database=mongo[config.MONGODB_DATABASE], document_models=document_models, allow_index_dropping=True)

	try:
		from faker import Faker
	except ImportError:
		pass
	else:
		faker = Faker()

		categories = {category.name: category for category in await ProductCategory.find_all().to_list()}

# 		await Product(
# 			name="WEERTI Thermal Underwear for Men Long Johns with Fleece Lined Base Layer Men Cold Weather Top Bottom",
# 			description="""All-Day Warmth: These long johns for men thermal lock in body heat for lasting warmth, keeping you comfortable through cold days as your reliable base layer all season long.
# Ultra-Soft Fleece: Made with premium fleece lining, this mens thermals top and bottom set provides a soft feel on the skin and lasting comfort from morning to night.
# Flexible Fit: Made with four-way stretch fabric, these long underwear mens deliver full mobility and comfort with no restriction or bunching, keeping you warm in all your activities.
# Dry Comfort Anywhere: These thermals for men are made of breathable fabric that quickly wicks away sweat and controls odor, keeping you dry and comfortable at home, office, gym, or outdoors.
# Layering Essential: This men's thermal underwear top and bottom set is a must-have base layer for cold weather. Layer under any outfit or wear as cozy pajamas for all-day warmth and comfort.""",
# 			category=categories["Underwear"],
# 			brand="WEERTI",
# 			gender=ProductGender.MEN,
# 			sizes=["M", "L", "XL"],
# 			stock=48,
# 			image_url="https://m.media-amazon.com/images/I/51-lXF3lDSL._AC_SX569_.jpg",
# 			price=Decimal("32.99"),
# 		).save()

	yield

app = fastapi.FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware())
app.include_router(api_router, prefix="/api")
app.include_router(templates_router)

def main() -> None:
	if os.name == "nt":
		asyncio.set_event_loop_policy(asyncio._WindowsSelectorEventLoopPolicy())

	uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)


if __name__ == "__main__":
	asyncio.run(main())
