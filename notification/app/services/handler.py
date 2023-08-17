"""
Обрабатывает, фильтрует поступающие события
для последующей передачи в очереди уведомлений
с базой данных разосланных уведомлений
"""
from functools import lru_cache
from abc import ABC, abstractmethod
import httpx
import json

from fastapi import Depends

from app.models import BasicEvent
from app.services.repository import AbstractRepository, get_repository
from app.services.rabbit_producer import get_producer, AbstractProducer
from app.core.config import config


class AbstractHandler(ABC):
    @abstractmethod
    def handle_single(event: BasicEvent):
        pass


class Handler(AbstractHandler):
    """
    Обрабатывает, фильтрует поступающие события
    для последующей передачи в очередь на рассылку уведомлений
    """

    def __init__(self, repository: AbstractRepository, producer: AbstractProducer):
        self.repository = repository
        self.producer = producer

    async def handle_single(self, event: BasicEvent):
        url = f'{config.auth_url}/{event.type_delivery}'
        headers = {'Authorization': config.auth_token, 'Content-Type': 'application/json'}

        if not event.email:
            data = json.dumps({'ids': str(event.user_id)})

            respone = httpx.post(url=url, headers=headers, data=data)
            event.email = respone.json().get('email')

        await self.repository.save_event(event)
        await self.producer.send_message(event)

    async def handle_multi(self, events: list[BasicEvent]):
        type_delivery = set([event.type_delivery for event in events])
        headers = {'Authorization': config.auth_token, 'Content-Type': 'application/json'}
        for type in type_delivery:
            url = f'{config.auth_url}/{type}'
            event_type = [event for event in events if event.type_delivery == type]
            ids = [event.user_id for event in event_type]
            data = json.dumps({'ids': ids})

            respone = httpx.post(url=url, headers=headers, data=data)
            dict_id_email = {elem['id']: elem['email'] for elem in respone.json()}
            for event in event_type:
                event.email = dict_id_email[str(event.user_id)]
                await self.repository.save_event(event)
                await self.producer.send_message(event)


@lru_cache()
def get_handler(
        repository: AbstractRepository = Depends(get_repository),
        producer: AbstractProducer = Depends(get_producer)
) -> AbstractHandler:
    return Handler(repository, producer)
