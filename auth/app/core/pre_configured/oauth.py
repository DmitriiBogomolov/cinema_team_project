from authlib.integrations.flask_client import OAuth

from app.core.config import google_config, yandex_config

oauth = OAuth()


yandex_client = oauth.register(
    **yandex_config.dict()
)


google_client = oauth.register(
    **google_config.dict()
)
