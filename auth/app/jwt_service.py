import json
from typing import Tuple, Optional
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

from app.token_storage import AbstractTokenStorage, RedisTokenStorage
from app.models import User


class JWTService:
    def __init__(self, storage: AbstractTokenStorage) -> None:
        self.storage = storage

    def create_tokens(self, payload: User) -> Tuple[str, str]:
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        return access_token, refresh_token

    def save_token(self, token: str) -> None:
        data_token = decode_token(token)
        user_data = data_token['sub']
        jti = data_token['jti']
        self.storage.save_user_token(self, user_data['id'], jti, json.dumps(user_data))

    def verify_token(self, jwt: dict) -> bool:
        user_data = jwt['sub']
        jti = jwt['jti']
        return self.storage.check_user_token(self, user_data['id'], jti)

    def revoke_token(self, jwt: dict, all: Optional[bool] = False) -> None:
        user_data = jwt['sub']
        jti = jwt['jti']
        if all:
            self.storage.delete_all_user_tokens(self, user_data['id'])
        self.storage.delete_user_token(self, user_data['id'], jti)


jwt_service = JWTService(RedisTokenStorage)
