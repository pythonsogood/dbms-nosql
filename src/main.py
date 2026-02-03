import asyncio
import os

from beanie import init_beanie
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

from models import Address, Order, Product, ProductCategory, User


async def main():
	client = AsyncMongoClient(os.getenv("MONGODB_CONNECTION"))

	await init_beanie(database=client[os.getenv("MONGODB_DATABASE")], document_models=[User, Address, ProductCategory, Product, Order])

	User(username="asd", email="asd", first_name="asd", last_name="asd", password_hash="asd", phone_number="asd", cart=[])

	while True:
		await asyncio.sleep(3)


if __name__ == "__main__":
	load_dotenv(".env")
	asyncio.run(main())
