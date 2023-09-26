"""
Предоставляет обработчик для события "получен новый комментарий к ревью"
"""
from functools import lru_cache
from abc import ABC, abstractmethod
import httpx
import json
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends
import jinja2
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.repository import AbstractRepository, get_repository
from app.services.rabbit_producer import get_producer, AbstractProducer
from app.handlers.common import AbstractHandler
from app.errors import WrongTemplateException
from app.base_models import BasicEvent


str_template = (
    '''
    Hello, {{user.email}}!
    '''
)

class User(BaseModel):
    id: UUID
    email: str

user = User(id='41e7bfbd-c0bc-4de2-902f-ba0f0c1eb501', email='hello@yandex.ru')


class ReviewCommentReceivedHandler(AbstractHandler):
    """
    Обработчик для события "получен новый комментарий к ревью"
    """

    def __init__(self, repository: AbstractRepository, producer: AbstractProducer):
        self.repository = repository
        self.producer = producer

    async def handle(self, event: BasicEvent):
        #url = f'{config.auth_url}/{event.type_delivery}'
        #headers = {'Authorization': config.auth_token, 'Content-Type': 'application/json'}

        # if not event.email:
        #     data = json.dumps({'ids': str(event.user_id)})

        #     respone = httpx.post(url=url, headers=headers, data=data)
        #     event.email = respone.json().get('email')


        # достаем шаблон из бд по имени, рендерим его

        template = jinja2.Template(str_template)
        try:    
            print(template.render({'user': user}))
        except jinja2.exceptions.UndefinedError:
            raise WrongTemplateException


        #await self.repository.save_event(event)
        #await self.producer.send_message(event)


@lru_cache()
def get_review_comment_received_handler(
        repository: AbstractRepository = Depends(get_repository),
        producer: AbstractProducer = Depends(get_producer)
) -> AbstractHandler:
    return ReviewCommentReceivedHandler(repository, producer)
