from enum import Enum
from uuid import uuid4, UUID

from pydantic import Field
from pydantic import BaseModel as PydanticBase


class EventNames(str, Enum):
    """Перечисляем имена принимаемых событий"""
    REVIEW_COMMENT_RECEIVED = 'review_comment_received'


class ServiceNames(str, Enum):
    """Перечисляем имена сервисов, от которых принимаются события"""
    AUTH_SERVICE = 'auth_service'


class ChannelNames(str, Enum):
    """Каналы рассылки используются классами конкретных событий (см. handlers)"""
    EMAIL = 'email'


class _CustomBase(PydanticBase):
    class Config:
        allow_population_by_field_name = True  # для преобразования в _id формат монги
        extra = 'allow'


class EventBase(_CustomBase):
    """Базовая схема, объединяющая поля, одинаковые для всех хендлеров"""
    id: UUID = Field(default_factory=lambda: str(uuid4()), alias='_id')
    initiating_service_name: ServiceNames  # сервис, вызвавший событие
    initiating_user_id: UUID | None  # пользователь, вызвавший событие
    description: str  # опциональное описание
    event_name: EventNames  # наименование события
    priority: int = Field(gte=0, lte=1)  # 0 для срочных, 1 для второстепенных
