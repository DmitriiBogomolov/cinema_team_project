"""
Обрабатывает, фильтрует поступающие события
для последующей передачи в очереди уведомлений
с базой данных разосланных уведомлений
"""
from functools import lru_cache
from abc import ABC, abstractmethod
from typing import Union, List
import httpx
import json

from fastapi import Depends

from app.models import BasicEvent
from app.services.repository import AbstractRepository, get_repository
from app.services.rabbit_producer import get_producer, AbstractProducer
from app.core.config import config


class AbstractHandler(ABC):
    @abstractmethod
    def handle_event(event: BasicEvent):
        pass


class Handler(AbstractHandler):
    """
    Обрабатывает, фильтрует поступающие события
    для последующей передачи в очередь на рассылку уведомлений
    """

    def __init__(self, repository: AbstractRepository, producer: AbstractProducer):
        self.repository = repository
        self.producer = producer

    async def handle_event(self, event: Union[BasicEvent, List[BasicEvent]]):
        headers = {'Authorization': config.auth_token, 'Content-Type': 'application/json'}

        if isinstance(event, list):
            type_delivery = set([ev.type_delivery for ev in event])
            for type in type_delivery:
                url = f'{config.auth_url}/{type}'
                event_type = [ev for ev in event if ev.type_delivery == type]
                ids = [ev.user_id for ev in event_type]
                data = json.dumps({'ids': ids})

                respone = httpx.post(url=url, headers=headers, data=data)
                dict_id_email = {elem['id']: elem['email'] for elem in respone.json()}
                for ev in event_type:
                    ev.email = dict_id_email[str(ev.user_id)]
                    await self.repository.save_event(ev)
                    await self.producer.send_message(ev)
        else:
            url = f'{config.auth_url}/{event.type_delivery}'
            if not event.email:
                data = json.dumps({'ids': str(event.user_id)})

                respone = httpx.post(url=url, headers=headers, data=data)
                event.email = respone.json().get('email')

            await self.repository.save_event(event)
            await self.producer.send_message(event)


@lru_cache()
def get_handler(
        repository: AbstractRepository = Depends(get_repository),
        producer: AbstractProducer = Depends(get_producer)
) -> AbstractHandler:
    return Handler(repository, producer)
