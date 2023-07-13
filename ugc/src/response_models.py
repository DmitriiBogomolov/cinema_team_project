from uuid import UUID
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId

from pydantic import BaseModel, Field


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, BsonObjectId) or isinstance(v, str):
            return str(v)
        else:
            raise TypeError('ObjectId required')


class BookmarkResponse(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    user_id: UUID
    movie_id: UUID
    created_at: datetime
