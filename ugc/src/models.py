from uuid import UUID

from pydantic import BaseModel, Field, validator


class ViewEventModel(BaseModel):
    movie_id: UUID
    lenght_movie: int = Field(ge=60, le=(24 * 60 * 60))  # total movie lenth
    duration: int = Field(ge=0)  # last viewed point of the movie (in seconds)

    @validator('duration')
    def must_be_lte_movie_lenght(cls, v, values, **kwargs):
        if values.get('lenght_movie') and v > values['lenght_movie']:
            raise ValueError('The current duration must be '
                             'lower or equal total movie lenght.')
        return v


class BookmarkModel(BaseModel):
    movie_id: UUID
