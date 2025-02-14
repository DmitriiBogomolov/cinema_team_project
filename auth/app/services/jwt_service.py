import json

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

from app.services.storage.token_storage import AbstractTokenStorage, RedisTokenStorage
from app.models import User
from app.schemas import ProfileSchema


profile_schema = ProfileSchema()


class JWTService:
    def __init__(self, storage: AbstractTokenStorage) -> None:
        self.storage = storage

    def create_tokens(self, user: User, expires=None) -> tuple[str, str]:
        user_data = profile_schema.dump(user)
        if user.is_superuser:
            user_data['top_secret'] = True
        access = create_access_token(user_data, expires_delta=expires)
        refresh = create_refresh_token(user_data, expires_delta=expires)
        return access, refresh

    def save_token(self, token: str | dict) -> None:
        token = self._decode_token(token)
        user_data = token['sub']
        jti = token['jti']
        self.storage.save_user_token(self, user_data['id'], jti, json.dumps(user_data))

    def verify_token(self, token: str | dict) -> bool:
        token = self._decode_token(token)
        user_id = token['sub']['id']
        jti = token['jti']
        return self.storage.check_user_token(self, user_id, jti)

    def revoke_token(self, token: str | dict) -> None:
        token = self._decode_token(token)
        user_id = token['sub']['id']
        jti = token['jti']
        self.storage.delete_user_token(self, user_id, jti)

    def revoke_user_tokens(self, user: User) -> None:
        self.storage.delete_all_user_tokens(self, user.id)

    def _decode_token(self, token: str | dict) -> dict:
        if isinstance(token, str):
            return decode_token(token)
        return token


jwt_service = JWTService(RedisTokenStorage)
