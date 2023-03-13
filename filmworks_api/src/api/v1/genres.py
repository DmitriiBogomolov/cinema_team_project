from typing import List

from fastapi import APIRouter

from .response_models import Genre

router = APIRouter()


@router.get('/', response_model=Genre)
async def get_genres_list() -> List[Genre]:
    pass
