from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class BasicModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias='_id')
    created_at: datetime = datetime.now()


class LikeModel(BasicModel):
    entity_id: UUID
    user_id: UUID
    rating: int


class ReviewModel(BasicModel):
    movie_id: UUID
    author_id: UUID
    text: str
    rating: float = 0
    likes_ids: list[UUID] = []


class BookmarkModel(BasicModel):
    user_id: UUID
    movie_id: UUID
