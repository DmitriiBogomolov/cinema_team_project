from enum import Enum
from uuid import uuid4, UUID
from datetime import datetime

from app.models.external import User

from pydantic import Field
from pydantic import BaseModel as PydanticBase


class ServiceNames(str, Enum):
    """Перечисляем имена сервисов, от которых принимаются события"""
    AUTH_SERVICE = 'auth_service'


class ChannelNames(str, Enum):
    """Перечисляем названия каналов для рассылки"""
    EMAIL = 'email'


class EventAPI(PydanticBase):
    """
    Базовая схема для ручки, содержащая поля,
    одинаковые для всех хендлеров
    """
    id: UUID = Field(default_factory=lambda: str(uuid4()), alias='_id')
    initiating_service_name: ServiceNames  # сервис, вызвавший событие
    initiating_user_id: UUID | None  # пользователь, вызвавший событие
    description: str  # опциональное описание
    event_name: str  # наименование события
    priority: int = Field(gte=0, lte=1, default=0)  # 0 для срочных, 1 для второстепенных
    channels: list[ChannelNames] = ['email']  # каналы рассылки

    class Config:
        extra = 'allow'


class Notification(EventAPI):
    """Модель, передаваемая в очередь"""
    recipient: User
    topic_message: str  # тема
    text_message: str  # отрендеренное сообщение
    created_at: datetime = Field(default_factory=datetime.now)
