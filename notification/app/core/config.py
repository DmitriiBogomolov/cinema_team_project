from enum import Enum

from pydantic import BaseSettings

from app.errors import WrongEventException
from app.handlers.review_comment_received import get_review_comment_received_handler
#from app.events import EventNames

"""
class EventNames(str, Enum):
    REVIEW_COMMENT_RECEIVED = 'review_comment_received'


class ServiceNames(str, Enum):
    AUTH_SERVICE = 'auth_service'


def get_event_handler(event_name):
    event_handlers = {
        EventNames.REVIEW_COMMENT_RECEIVED: get_review_comment_received_handler()
    }

    handler = event_handlers.get(event_name)
    if not handler:
        raise WrongEventException
    return handler
"""

class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class AppConfig(Base):
    project_name: str = 'notification_service'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    debug: bool = True

    authjwt_secret_key: str
    auth_url: str
    auth_token: str


class MongoConfig(Base):
    uri: str

    class Config:
        env_prefix = 'mongo_'


class RabbitConfig(Base):
    uri: str

    class Config:
        env_prefix = 'rabbit_'


config = AppConfig()
mongo_config = MongoConfig()
rabbit_config = RabbitConfig()
