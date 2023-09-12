from functools import lru_cache
from abc import ABC, abstractmethod
import httpx

from flask import (
    request,
    redirect,
    url_for
)

from app.schemas import (
    UserSchema,
)

from app.models import User
from app.core.logger import logger
from app.helpers.tokens import generate_token
from app.model_api import ConfirmLetter
from app.core.config import config


user_schema = UserSchema()


class AbstractUserNotificator(ABC):
    @abstractmethod
    def send_confirm_letter():
        pass


class UserNotificator(AbstractUserNotificator):
    """
    Предназначен для рассылки уведомлений пользователю
    """
    async def send_confirm_letter(user: User):
        user = user_schema.dump(user)
        token = generate_token(user['email'])
        reference = f'{request.environ["HTTP_ORIGIN"]}/api/v1/confirm_letter/{token}'
        event_data = ConfirmLetter(user_id=user['id'], email=user['email'], text_message=reference)
        url = config.uri_notification
        headers = {
            'Authorization': config.token_notification,
            'Content-Type': 'application/json',
            'X-Request-Id': request.headers.get('X-Request-Id')
        }
        try:
            resp = httpx.post(url, headers=headers, data=event_data.json)
            logger.info(f'{resp.status_code}-{resp.text}')
        except httpx.ConnectError:
            redirect(url_for('auth.user_registration'))


@lru_cache()
def get_user_notificator() -> AbstractUserNotificator:
    return UserNotificator()


user_notificator = UserNotificator()
