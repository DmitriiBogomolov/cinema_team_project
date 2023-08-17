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


class BasicEvent(_Base):
    """Основная форма хранимого события"""
    id: CustomUuid = Field(default_factory=lambda: str(uuid4()), alias='_id')
    user_id: CustomUuid
    email: EmailStr | None
    event_name: str
    topic_message: str
    text_message: str
    type_delivery: str
    priority: bool
    created_at: datetime = Field(default_factory=datetime.now)
    send_message_datatime: datetime | None

    def to_mongo(self):
        """
        Обогощает документ хранимого события полем recipient_id
        для индексации и поиска по отправителям
        """
        me = self.dict(by_alias=True)
        return me
