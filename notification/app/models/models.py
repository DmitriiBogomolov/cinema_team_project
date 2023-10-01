from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from pydantic import Field, EmailStr
from pydantic import BaseModel as PydanticBase

from app.models.core import EventBase


SqlalchemyBase = declarative_base()  # Точка входа в sqlchemy


class EmailTemlate(SqlalchemyBase):
    """Хранимые шаблоны уведомлений (sqlalchemy + postgresql)"""
    __tablename__ = "email_templates"

    event_name = Column(String, primary_key=True, nullable=False)
    topic_message = Column(String, nullable=False)
    template = Column(String, nullable=False)


class User(PydanticBase):
    id: UUID
    email: EmailStr | None


class Notification(EventBase):
    """Модель для хранения уведомления в mongodb и передачи в очередь"""
    recipient: User
    topic_message: str  # тема
    text_message: str  # отрендеренное сообщение
    send_message_datatime: datetime | None = None  # отправлено ли уведомление
    created_at: datetime = Field(default_factory=datetime.now)
