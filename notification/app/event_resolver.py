from functools import lru_cache

from fastapi import Depends
from app.errors import WrongEventException
from app.handlers.review_comment_received import (
    get_review_comment_received_handler,
    ReviewCommentReceivedHandler
)
from app.models.core import EventNames


class EventResolver:
    """ Предназначен для сопоставления срабатываемых событий с обработчиками"""
    def __init__(
        self,
        review_comment_received_handler: ReviewCommentReceivedHandler
    ):
        """Сюда регистрируем обработчики"""
        self.event_handlers = {
            EventNames.REVIEW_COMMENT_RECEIVED: review_comment_received_handler
        }

    async def get_handler(self, event_name: str):
        """Предоставляет обработчик по названию события"""
        handler = self.event_handlers.get(event_name)
        if not handler:
            raise WrongEventException
        return handler


@lru_cache()
def get_event_resolver(
        review_comment_received_handler = Depends(get_review_comment_received_handler),
) -> EventResolver:
    return EventResolver(
        review_comment_received_handler
    )
