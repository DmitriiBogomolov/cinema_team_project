"""
Базовый обработчик для типовых событий
"""
from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rabbit_producer import (
    get_producer,
    AbstractProducer
)
from app.handlers.common import AbstractHandler
from app.errors import WrongTemplateException
from app.models.core import EventAPI
from app.template_engine import render_email
from app.db.postgres import get_pg_session
from app.models.core import ChannelNames, Notification
from app.models.models import EmailTemlate
from app.models.external import User


class DefaultEvent(EventAPI):
    """
    Расширяем/переопределяем схему для валидации
    события в хендлере (в данном случае - для типовых событий)
    """
    user_ids: list[UUID]  # айдишники адресатов


class DefaultHandler(AbstractHandler):
    """
    Получает шаблоны из БД
    рендерит и загружает уведомления в очередь
    """
    def __init__(
            self,
            producer: AbstractProducer,
            pg_session: AsyncSession
    ):
        self.producer = producer
        self.pg_session = pg_session

    async def _process_email(self, event: DefaultEvent):
        # Получаем шаблон и тему из БД
        email_template = await self.pg_session.get(
            EmailTemlate,
            event.event_name
        )
        if not email_template:
            raise WrongTemplateException
        email_teplate_str = email_template.template
        email_topic_message = email_template.topic_message

        # Получаем пользователей
        users = User.get_list(event.user_ids)

        # Подготавливаем данные для рендера
        render_data = [{'user': user.dict()} for user in users]

        # Рендерим уведомления
        email_body_list = await render_email(
            render_data,
            email_teplate_str
        )

        # загружаем нотификации в соответствующую очередь
        for user, message in zip(users, email_body_list):
            notification = Notification(
                recipient=user,
                topic_message=email_topic_message,
                text_message=message,
                **event.dict()
            )
            await self.producer.send_message(notification, 'email')

    async def handle(self, event: EventAPI):
        if ChannelNames.EMAIL in event.channels:
            await self._process_email(event)


@lru_cache()
def get_default_handler(
        producer: AbstractProducer = Depends(get_producer),
        pg_session: AsyncSession = Depends(get_pg_session)
) -> AbstractHandler:
    return DefaultHandler(producer, pg_session)
