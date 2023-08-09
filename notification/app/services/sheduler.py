"""
Обрабатывает, фильтрует поступающие события
для последующей передачи в очереди уведомлений
с базой данных разосланных уведомлений
"""
from functools import lru_cache
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from fastapi import Depends

from app.models import (
    _BasicSingleEvent, _BasicMultipleEvent,
    SingleNewReviewLike, MultipleTemplateMailing,
    MultipleBookmarksReminder
)
from app.services.repository import AbstractRepository, get_repository
from app.services.rabbit_producer import get_producer, AbstractProducer
from app.errors import WrongEventException


class AbstractSheduler(ABC):
    @abstractmethod
    def handle_single(event: _BasicSingleEvent):
        pass

    @abstractmethod
    def handle_multiple(event: _BasicMultipleEvent):
        pass


class Sheduler(AbstractSheduler):
    """
    Обрабатывает, фильтрует поступающие события
    для последующей передачи в очередь на рассылку уведомлений
    """

    def __init__(self, repository: AbstractRepository, producer: AbstractProducer):
        self.repository = repository
        self.producer = producer

    async def handle_single(self, event: _BasicSingleEvent):
        if isinstance(event, SingleNewReviewLike):
            """
            Одиночное событие нового лайка на review пользователя
            Отрпавляем не дублирующие события,
            по одному в сутки на каждое ревью пользователя
            """
            event_name = 'review_like_received'
            event.set_event_name(event_name)

            event_type = 'email'
            event.set_event_type(event_type)

            # проверка на дублирующее событие
            count_1 = await self.repository.count({
                'event_name': event_name,
                'recipient_data._id': str(event.recipient_data.id),
                'recipient_data.review_id': str(event.recipient_data.review_id),
                'recipient_data.like_owner_id': str(event.recipient_data.like_owner_id),
            })

            # проверка на наличие отправленного уведомления по указанному
            # review, произошедшее в течении дня
            count_2 = await self.repository.count({
                'event_name': event_name,
                'recipient_data._id': str(event.recipient_data.id),
                'recipient_data.review_id': str(event.recipient_data.review_id),
                'created_at': {'$gte': datetime.now() - timedelta(days=1)}
            })

            if count_1 or count_2:
                raise WrongEventException

            await self.repository.save_single(event)
            await self.producer.send_message(event_type, event)

    async def handle_multiple(self, event: _BasicMultipleEvent):
        if isinstance(event, MultipleTemplateMailing):
            """
            Множественная рассылка по предложенному шаблону,
            отправляем все недублирующие события
            """
            event_name = 'mail_multiple'
            event.set_event_name(event_name)

            event_type = 'email'
            event.set_event_type(event_type)

            if await self.repository.count({
                'event_name': event_name,
                'multiple_event_id': str(event.multiple_event_id),
            }):
                raise WrongEventException

            await self.repository.save_multiple(event)
            await self.producer.send_message(event_type, event)

        if isinstance(event, MultipleBookmarksReminder):
            """
            Множественная рассылка уведомлений об отложенных фильмах.
            Отправляем недублирующие события, если в течении двух недель пользователь
            не добавлял новых закладок и при этом последнее аналогичное
            уведомление не отправлялось последние 6 недель
            """
            event_name = 'bookmarks_reminder_multiple'
            event.set_event_name(event_name)

            event_type = 'email'
            event.set_event_type(event_type)

            await self.repository.save_multiple(event)
            await self.producer.send_message(event_type, event)


@lru_cache()
def get_sheduler(
        repository: AbstractRepository = Depends(get_repository),
        producer: AbstractProducer = Depends(get_producer)
) -> AbstractSheduler:
    return Sheduler(repository, producer)
