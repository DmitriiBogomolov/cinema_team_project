from uuid import UUID

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class UUIDModel(BaseModel):
    """Core schema object."""
    id: UUID = Field(alias='uuid')

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
