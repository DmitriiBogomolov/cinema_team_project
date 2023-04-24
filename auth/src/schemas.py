from app import ma
from src.models import User, Session

from marshmallow import fields, post_load
from werkzeug.security import generate_password_hash

from src.utils.validators import password_validator


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_only = ['password']
        dump_only = ['id']

    id = fields.UUID(required=True)
    email = fields.Email(required=True)

    password = fields.String(
        required=True,
        validate=password_validator
    )

    @post_load
    def make_obj(self, data, **kwargs):
        data['password'] = generate_password_hash(
            password=data['password'],
            method='pbkdf2:sha512',
            salt_length=16
        )
        return User(**data)


class UserJWTPayloadSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()


class SessionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Session
        dump_only = ['id']

    user_id = ma.auto_field()
    user_agent = fields.Raw()
    remote_addr = fields.IP(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return Session(
            user_id=data['user_id'],
            agent_platform=data['user_agent'].platform,
            agent_browser=data['user_agent'].browser,
            agent_version=data['user_agent'].version,
            agent_language=data['user_agent'].language,
            agent_string=data['user_agent'].string,
            remote_addr=data['remote_addr'].exploded
        )
