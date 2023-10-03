"""
Предоставляет обработчик для события "получен новый комментарий к ревью"
"""
from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.repository import AbstractRepository, get_repository
from app.services.rabbit_producer import get_producer, AbstractProducer
from app.handlers.common import AbstractHandler
from app.errors import WrongTemplateException
from app.models.core import EventBase
from app.template_engine import render_email
from app.db.postgres import get_pg_session
from app.models.models import EmailTemlate, Notification, User


#########################################################
# для отработки в postgresql нужно добавить шаблон для события
# event_name: 'review_comment_received'
# topic_message: любое
# template_str: 'Hello, {{user.email}}!'
#########################################################
#########################################################


class ReviewCommentReceivedEvent(EventBase):
    """Дополнительно настрает сигнатуру обработчика"""
    user_ids: list[UUID]


class ReviewCommentReceivedHandler(AbstractHandler):
    """
    Обработчик для события \"получен новый комментарий к ревью\"
    Ожидается, что через ручку пройдет:
    {
        "initiating_service_name": "auth_service",
        "initiating_user_id": "6b7aae84-517d-11ee-be56-0242ac120002",
        "description": "some_description",
        "event_name": "review_comment_received",
        "priority": 0,
        "user_ids": ["6b7aae84-517d-11ee-be56-0242ac120002"]
    }
    """
    def __init__(
            self,
            repository: AbstractRepository,
            producer: AbstractProducer,
            pg_session: AsyncSession
    ):
        self.repository = repository
        self.producer = producer
        self.pg_session = pg_session

    async def handle(self, event: ReviewCommentReceivedEvent):

        # Получаем шаблон и тему из БД
        email_template = await self.pg_session.get(EmailTemlate, event.event_name)
        if not email_template:
            raise WrongTemplateException
        email_teplate_str = email_template.template
        email_topic_message = email_template.topic_message

        # Подготавливаем данные для рендера (вместо этого будем регать auth)
        mock_user = User(id='41e7bfbd-c0bc-4de2-902f-ba0f0c1eb501', email='hello@yandex.ru')
        users = [mock_user for _ in event.user_ids]
        render_data = [{'user': user.dict()} for user in users]

        # Рендерим уведомления
        email_body_list = await render_email(
            render_data,
            email_teplate_str
        )

        # создаем нотификации
        # notifications = [
        #     Notification(
        #         recipient=user,
        #         topic_message=email_topic_message,
        #         text_message=message,
        #         **event.dict()
        #     ) for user, message in zip(users, email_body_list)
        # ]

        # далее нужно эти нотификации сохранить и отправить в очередь емейл рассылок
        for user, message in zip(users, email_body_list):
            notification = Notification(
                recipient=user,
                topic_message=email_topic_message,
                text_message=message,
                **event.dict()
            )
            await self.producer.send_message(notification, 'email')
        # await self.repository ... сохранить нотификации
        # await self.producer ... запустить дальше в очередь


@lru_cache()
def get_review_comment_received_handler(
        repository: AbstractRepository = Depends(get_repository),
        producer: AbstractProducer = Depends(get_producer),
        pg_session: AsyncSession = Depends(get_pg_session)
) -> AbstractHandler:
    return ReviewCommentReceivedHandler(repository, producer, pg_session)
