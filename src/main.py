import asyncio
import os
from contextlib import asynccontextmanager

import fastapi
import uvicorn
from beanie import init_beanie

import config
from api import dependencies, router as api_router
from models import Address, Order, Product, ProductCategory, User


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
	mongo = dependencies.database()

	document_models = [User, Address, ProductCategory, Product, Order]

	await init_beanie(database=mongo[config.MONGODB_DATABASE], document_models=document_models, allow_index_dropping=True)

	yield


app = fastapi.FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")

def main() -> None:
	if os.name == "nt":
		asyncio.set_event_loop_policy(asyncio._WindowsSelectorEventLoopPolicy())

	uvicorn.run(app, host="0.0.0.0", port=config.PORT)


if __name__ == "__main__":
	asyncio.run(main())
