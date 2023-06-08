from authlib.integrations.flask_client import OAuth

oauth = OAuth()

yandex = oauth.register(
    name='yandex',
    client_id='06fa5191cc8246f99dbe93f662de085d',
    client_secret='38d1ea900ff542499ad1250894b51f6d',
    authorize_url='https://oauth.yandex.ru/authorize',
    access_token_url='https://oauth.yandex.ru/token'
)
