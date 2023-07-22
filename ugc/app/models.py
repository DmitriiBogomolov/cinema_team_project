import json
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class BasicModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias='_id')
    created_at: datetime = datetime.now()

    def to_doc(self):
        return json.loads(self.json(by_alias=True))


class LikeModel(BasicModel):
    entity_id: UUID
    user_id: UUID
    rating: int


class ReviewModel(BasicModel):
    movie_id: UUID
    user_id: UUID
    text: str
    likes: list[dict] = []


class BookmarkModel(BasicModel):
    user_id: UUID
    movie_id: UUID
