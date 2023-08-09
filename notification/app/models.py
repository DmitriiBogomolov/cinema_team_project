"""
Модуль с задействованными моделями событий
используется для валидации поступающих данных о событиях
и их преобразования для хранения в репозитории
"""


from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from app.model_fields import CustomUuid


class _Base(BaseModel):
    class Config:
        allow_population_by_field_name = True  # для преобразования в _id формат монги


class _BasicEvent(_Base):
    """Основная форма хранимого события"""
    id: CustomUuid = Field(default_factory=lambda: str(uuid4()), alias='_id')
    sender_service: str = Field(min_length=0, max_length=255)
    trigger_user_id: CustomUuid | None
    description: str = Field(min_length=0, max_length=1020)
    created_at: datetime = Field(default_factory=datetime.now)
    send_message_datatime: datetime | None
    event_name: str | None
    event_type: str | None

    def set_event_name(self, event_name: str):
        self.event_name = event_name

    def set_event_type(self, event_type: str):
        self.event_type = event_type


class _BasicSingleEvent(_BasicEvent):
    """Базовая модель для одиночных рассылок"""
    def to_mongo(self):
        """
        Обогощает документ хранимого события полем recipient_id
        для индексации и поиска по отправителям
        """
        me = self.dict(by_alias=True)
        me['recipient_id'] = me['recipient_data']['_id']
        return me


class _BasicMultipleEvent(_BasicEvent):
    """Базовая модель для множественных рассылок"""
    multiple_event_id: CustomUuid  # должен быть передан для идентификации составляющих событий

    def to_mongo(self):
        """
        Разбивает событие множественной рассылки на соответствующие
        документы событий + обогощает необходимыми полями
        """
        result = []
        for recipient in self.recipient_data:
            event = self.dict(by_alias=True)
            event['_id'] = str(uuid4())
            event['recipient_id'] = recipient.id
            event['recipient_data'] = recipient.dict(by_alias=True)
            result.append(event)
        return result


class SingleNewReviewLike(_BasicSingleEvent):
    """
    Модель события единичного уведомления при
    поставленном лайке на рецензию пользователя
    """
    class RecipientData(_Base):
        id: CustomUuid = Field(alias='_id')  # recipient id (those review owner id)
        email: EmailStr
        priority: int = Field(ge=-1, le=2)
        like_owner_id: CustomUuid  # user who liked
        review_id: CustomUuid
        review_movie_id: CustomUuid
        review_text: str
        review_likes: int
        review_created_at: datetime
    recipient_data: RecipientData


class MultipleTemplateMailing(_BasicMultipleEvent):
    """
    Модель события для массовой рассылки
    по предложенному шаблону
    """
    class RecipientData(_Base):
        id: CustomUuid = Field(alias='_id')  # recipient id
        email: EmailStr
        priority: int = Field(ge=-1, le=2)
    recipient_data: list[RecipientData]
    template: str


class MultipleBookmarksReminder(_BasicMultipleEvent):
    """
    Модель события для массовой рассылки уведомлений
    об отложенных фильмах пользователям
    """
    class RecipientData(_Base):
        class Bookmark(_Base):
            id: CustomUuid = Field(alias='_id')  # bookmark id
            title: str
            imdb_rating: float | None = None
            description: str | None = None
            genres: list[str]

        id: CustomUuid = Field(alias='_id')  # recipient id
        email: EmailStr
        priority: int = Field(ge=-1, le=2)
        bookmarks: list[Bookmark]

    recipient_data: list[RecipientData]
