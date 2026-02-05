from pymongo import AsyncMongoClient

import config


class Database():
	def __init__(self, connection: str) -> None:
		self._mongo = AsyncMongoClient(connection, tz_aware=True)

	def __call__(self) -> AsyncMongoClient:
		return self._mongo


database = Database(config.MONGODB_CONNECTION)
