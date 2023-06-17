from dataclasses import dataclass

from authlib.integrations.flask_client import OAuth
from pydantic import BaseSettings
from werkzeug.exceptions import NotFound

from app.core.config import google_config, yandex_config

oauth = OAuth()


class _Provider:
    def __init__(self, config: BaseSettings):
        self.name = config.name
        self.config = config
        self.client = oauth.register(**config.dict())

    def get_user_info(self) -> dict:
        token = self.client.authorize_access_token()
        user_data = self.client.get(
            self.config.user_info_url,
            token=token
        ).json()
        return user_data


@dataclass
class _Providers:
    yandex: _Provider
    google: _Provider

    def get(self, provider_name: str) -> _Provider:
        if not provider_name or not hasattr(self, provider_name):
            raise NotFound
        return getattr(self, provider_name)


providers = _Providers(
    yandex=_Provider(yandex_config),
    google=_Provider(google_config)
)
