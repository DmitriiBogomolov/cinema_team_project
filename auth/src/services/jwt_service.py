from flask_jwt_extended import create_access_token, create_refresh_token

from src.schemas import UserSchema, UserJWTPayloadSchema, LoginEntrieSchema
from src.models import User
from src.exceptions import RevokedTokenError
from app import app, refresh_blacklist


user_schema = UserSchema()
user_payload_schema = UserJWTPayloadSchema()  # repr user data in jwt
entrie_schema = LoginEntrieSchema()  # repr one record of logins history


class JWTService():
    def create_jwt_pair(self, user: User) -> dict:
        """Create jwt pair for provided user"""
        user_payload = user_payload_schema.dump(user)
        return {
            'access': create_access_token(identity=user_payload),
            'refresh': create_refresh_token(identity=user_payload)
        }

    def refresh_jwt_pair(self, refresh_token: dict) -> dict:
        """Provide token pair instead of refresh token"""

        self.check_in_blocklist(refresh_token)
        user = User.query.get(refresh_token['sub']['id'])
        self.revoke_token(refresh_token)
        return self.create_jwt_pair(user)

    def revoke_token(self, token: dict) -> None:
        """Append token to blocklist"""
        self.check_in_blocklist(token)

        jti = token['jti']
        refresh_blacklist.set(jti, '', ex=app.config['JWT_REFRESH_TOKEN_EXPIRES'])

    def check_in_blocklist(self, token: dict) -> None:
        """Checks if token in blocklist."""
        jti = token['jti']

        if refresh_blacklist.exists(jti):
            raise RevokedTokenError


jwt_service = JWTService()
