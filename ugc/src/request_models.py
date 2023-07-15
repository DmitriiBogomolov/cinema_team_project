from uuid import UUID

from pydantic import BaseModel, Field, validator


class ViewEventRequestModel(BaseModel):
    movie_id: UUID
    lenght_movie: int = Field(ge=60, le=(24 * 60 * 60))  # total movie lenth
    duration: int = Field(ge=0)  # last viewed point of the movie (in seconds)

    @validator('duration')
    def must_be_lte_movie_lenght(cls, v, values, **kwargs):
        if values.get('lenght_movie') and v > values['lenght_movie']:
            raise ValueError('The current duration must be '
                             'lower or equal total movie lenght.')
        return v


class LikeRequestModel(BaseModel):
    entity_id: UUID
    rating: int = Field(ge=0, le=10)


class ReviewRequestModel(BaseModel):
    movie_id: UUID
    text: str


class BookmarkRequestModel(BaseModel):
    movie_id: UUID
