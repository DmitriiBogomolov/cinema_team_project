from enum import Enum

from app.errors import WrongEventException
from app.handlers.review_comment_received import get_review_comment_received_handler
from app.base_models import EventNames


def get_event_handler(event_name):
    """Сопоставляет событию обработчик"""
    event_handlers = {
        EventNames.REVIEW_COMMENT_RECEIVED: get_review_comment_received_handler()
    }

    handler = event_handlers.get(event_name)
    if not handler:
        raise WrongEventException
    return handler
