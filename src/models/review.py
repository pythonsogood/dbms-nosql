import datetime
from typing import Annotated

from annotated_types import Interval
from pydantic import BaseModel, Field


class Review(BaseModel):
	username: str
	rating: Annotated[int, Interval(ge=1, le=5)]
	comment: str
	created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))
