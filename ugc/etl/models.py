from datetime import datetime
from pydantic import BaseModel


class TableViews(BaseModel):
    user_id: str
    movie_id: str
    duration: int
    lenght_movie: int
    event_time: datetime
