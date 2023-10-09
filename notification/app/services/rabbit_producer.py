"""Producer занимается отправкой событий в очередь для далнейшей обработки"""
from functools import lru_cache
from abc import ABC, abstractmethod
from fastapi import Depends
from aio_pika import Connection, Message, Exchange
from app.db.rabbit import get_rabbit_producer
from app.models.core import EventAPI


class AbstractProducer(ABC):
    @abstractmethod
    async def send_message(self, *args, **kwargs):
        pass


class Producer(AbstractProducer):
    def __init__(self, exchange: Exchange) -> None:
        self.exchange = exchange

    async def send_message(self, message: EventAPI, queue: str):
        await self.exchange.publish(
            Message(message.json().encode(), priority=message.priority), queue)


@lru_cache()
def get_producer(
        rabbit: Connection = Depends(get_rabbit_producer),
) -> AbstractProducer:
    return Producer(rabbit)
