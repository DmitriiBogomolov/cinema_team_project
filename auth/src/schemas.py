from src import ma
from src.models import User

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
