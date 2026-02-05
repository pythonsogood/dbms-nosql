import datetime
import logging

import argon2
import jwt
import pymongo
from beanie import Document, Link
from pydantic import EmailStr, Field
from pymongo import IndexModel

import config

from .product import Product


PASSWORD_HASHER = argon2.PasswordHasher(time_cost=2, memory_cost=19 * 1024, parallelism=1)


class User(Document):
	username: str
	email: EmailStr
	first_name: str
	last_name: str | None = None
	role: str = "customer"
	password_hash: str
	phone_number: str | None = None
	cart: list[Link[Product]] = Field(default_factory=list)
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))

	class Settings:
		name = "users"
		use_state_management = True
		indexes = [
			IndexModel([("username", pymongo.ASCENDING)], unique=True),
			IndexModel([("email", pymongo.ASCENDING)], unique=True),
		]

	@staticmethod
	def hash_password(password: str) -> str:
		return PASSWORD_HASHER.hash(password)

	@staticmethod
	def verify_password_with(password: str, password_hash: str) -> bool:
		try:
			return PASSWORD_HASHER.verify(password_hash, password)
		except argon2.exceptions.VerificationError:
			return False

	def verify_password(self, password: str) -> bool:
		try:
			return User.verify_password_with(password, self.password_hash)
		except argon2.exceptions.InvalidHashError as e:
			logging.error(f"Hashing error for user {self.username}: {repr(e)}")
			return False

	def create_jwt_token(self) -> str:
		return jwt.encode({
			"sub": str(self.id),
			"exp": datetime.datetime.now(tz=datetime.UTC) + config.JWT_TOKEN_EXPIRATION,
		}, config.JWT_SECRET_KEY, "HS256")
