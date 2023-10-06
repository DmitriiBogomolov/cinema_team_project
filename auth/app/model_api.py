from pydantic import BaseModel, EmailStr
from pydantic.dataclasses import dataclass
from dataclasses import asdict
from json import dumps


class RecipientData(BaseModel):
    id: str  # recipient id
    email: EmailStr
    priority: int = 1
    message_data: str


@dataclass
class ConfirmLetter:
    """Основная форма хранимого события"""
    user_id: str = None
    email: EmailStr = None
    priority: int = 1
    event_name: str = 'Welcome'
    type_delivery: str = 'email'
    topic_message: str = None
    text_message: str = None

    def __post_init__(self):
        self.topic_message = 'Welcome %s' % (self.email)
        self.text_message = 'Для подтверждения электронной почты перейдите по ссылке %s' % (self.text_message)

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return dumps(self.__dict__)


class ContactsUser(BaseModel):
    id: str
    email: str
