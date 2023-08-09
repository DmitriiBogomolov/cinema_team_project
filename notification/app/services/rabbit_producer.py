"""Producer занимается отправкой событий в очередь для далнейшей обработки"""

from typing import Union
from functools import lru_cache
from abc import ABC, abstractmethod
from fastapi import Depends
from aio_pika import Connection, Message, Exchange
from app.db.rabbit import get_rabbit_producer
from app.models import _BasicSingleEvent, _BasicMultipleEvent


class AbstractProducer(ABC):
    @abstractmethod
    async def send_message(self, *args, **kwargs):
        pass


class Producer(AbstractProducer):
    def __init__(self, exchange: Exchange) -> None:
        self.exchange = exchange

    async def send_message(self, queue_name: str, data: Union[_BasicSingleEvent, _BasicMultipleEvent]):
        messages = data.recipient_data

        if isinstance(messages, list):
            for message in messages:
                await self.exchange.publish(
                    Message(message.json().encode()), queue_name
                )
        else:
            await self.exchange.publish(
                Message(messages.json().encode()), queue_name
            )


@lru_cache()
def get_producer(
        rabbit: Connection = Depends(get_rabbit_producer),
) -> AbstractProducer:
    return Producer(rabbit)
