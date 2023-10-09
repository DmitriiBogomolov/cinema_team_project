from functools import lru_cache

from fastapi import Depends
from app.handlers.default import (
    get_default_handler,
    DefaultHandler,
)


class EventResolver:
    """
    Предназначен для сопоставления срабатываемых
    событий с обработчиками
    """
    def __init__(
        self,
        default_handler: DefaultHandler
    ):
        """
        Сюда регистрируем обработчики
        """
        self.event_handlers = {}

        self.default_handler = default_handler

    async def get_handler(self, event_name: str):
        """
        Предоставляет обработчик по названию события,
        по-умолчанию предоставляет default handler
        """
        handler = self.event_handlers.get(event_name)
        return handler or self.default_handler


@lru_cache()
def get_event_resolver(
        default_handler=Depends(get_default_handler)
) -> EventResolver:
    return EventResolver(
        default_handler
    )
