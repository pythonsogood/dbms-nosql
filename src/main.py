import asyncio
import os
from contextlib import asynccontextmanager

import fastapi
import uvicorn
from beanie import init_beanie
from fastapi.staticfiles import StaticFiles

import config
from api import api_router, dependencies, templates_router
from models import Address, Order, Product, ProductCategory, User


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
	mongo = dependencies.database()

	document_models = [User, Address, ProductCategory, Product, Order]

	await init_beanie(database=mongo[config.MONGODB_DATABASE], document_models=document_models, allow_index_dropping=True)

	yield

app = fastapi.FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api")
app.include_router(templates_router)

def main() -> None:
	if os.name == "nt":
		asyncio.set_event_loop_policy(asyncio._WindowsSelectorEventLoopPolicy())

	uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)


if __name__ == "__main__":
	asyncio.run(main())
