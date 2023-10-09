"""
Обработчик ручной рассылки уведомлений по переданому шаблону
"""
from functools import lru_cache

from fastapi import Depends

from app.services.rabbit_producer import get_producer, AbstractProducer
from app.handlers.common import AbstractHandler
from app.models.core import EventAPI
from app.template_engine import render_email
from app.models.core import Notification
from app.models.external import User


class ManualMailEvent(EventAPI):
    topic_message: str  # Тема рассылки
    email_template: str | None = None  # Шаблон


class ManualMailHandler(AbstractHandler):
    """
    Обработчик ручной рассылки уведомлений по переданому шаблону
    """
    def __init__(
            self,
            producer: AbstractProducer
    ):
        self.producer = producer

    async def _process_email(self, event: ManualMailEvent):
        # Получаем пользователей
        users = User.get_list(event.user_ids)

        # Подготавливаем данные для рендера
        render_data = [{'user': user.dict()} for user in users]

        # Рендерим уведомления
        email_body_list = await render_email(
            render_data,
            event.email_template
        )

        # загружаем нотификации в соответствующую очередь
        for user, message in zip(users, email_body_list):
            notification = Notification(
                recipient=user,
                topic_message=event.topic_message,
                text_message=message,
                **event.dict()
            )
            await self.producer.send_message(notification, 'email')

    async def handle(self, event: EventAPI):
        if event.email_template:
            await self._process_email(event)


@lru_cache()
def get_manual_mail_handler(
        producer: AbstractProducer = Depends(get_producer)
) -> AbstractHandler:
    return ManualMailHandler(producer)
