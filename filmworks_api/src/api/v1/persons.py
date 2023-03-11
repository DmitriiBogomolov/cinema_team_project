from fastapi import APIRouter

from .response_models import PersonDetail


router = APIRouter()


@router.get('/{person_id}')
async def get_person_detail(person_id: str) -> PersonDetail:
    pass
