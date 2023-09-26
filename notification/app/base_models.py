"""
Модуль с задействованными моделями событий
используется для валидации поступающих данных о событиях
и их преобразования для хранения в репозитории
"""
from enum import Enum
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class EventNames(str, Enum):
    """Перечисляем имена принимаемых событий"""
    REVIEW_COMMENT_RECEIVED = 'review_comment_received'


class ServiceNames(str, Enum):
    """Перечисляем имена сервисов, от которых принимаются события"""
    AUTH_SERVICE = 'auth_service'


class _Base(BaseModel):
    class Config:
        allow_population_by_field_name = True  # для преобразования в _id формат монги
        extra = 'allow'


class NotificationData(_Base):
    """
    Уникальные и минимально необходимые данные планируемого уведомления
    для последующего обогащения и рендера
    """
    recipient_id: UUID
    # ... что-то еще


class BasicEvent(_Base):
    """
    Событие с пачкой планируемых уведомлений (минимально необходимых данных)
    принимаемое в API
    """
    id: UUID = Field(default_factory=lambda: str(uuid4()), alias='_id')
    initiating_service_name: ServiceNames # сервис, вызвавший событие
    initiating_user_id: UUID | None  # пользователь, вызвавший событие
    description: str # опциональное описание
    event_name: EventNames # наименование события
    priority: int = Field(gte=0, lte=1) # 0 для срочных, 1 для второстепенных
    notifications_data: list[NotificationData] # пачка с данными уведомлений
