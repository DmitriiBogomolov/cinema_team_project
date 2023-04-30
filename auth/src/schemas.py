from app import ma
from src.models import User, LoginEntrie, Role

from marshmallow import (fields,
                         post_load,
                         Schema,
                         ValidationError,
                         validates_schema)
from werkzeug.security import generate_password_hash

from src.validators import password_validator


class NotEmptySchema:
    @validates_schema
    def validate_no_data(self, data, **kwargs):
        if not data:
            raise ValidationError('No provided data.')


class UserSchema(ma.SQLAlchemySchema):
    """User registration schema and getting standard data."""

    class Meta:
        model = User
        load_only = ['password']
        dump_only = ['id', 'roles']

    id = fields.UUID(required=True)
    email = fields.Email(required=True)
    roles = ma.Nested('RoleSchema', many=True)

    password = fields.String(
        required=True,
        validate=password_validator
    )

    @post_load
    def make_obj(self, data: dict, **kwargs) -> User:
        data['password'] = generate_password_hash(data['password'])
        return User(**data)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return generate_password_hash(
            password=password,
            method='pbkdf2:sha512',
            salt_length=16
        )


class UpdateUserSchema(ma.SQLAlchemySchema):
    """Schema for updating user data."""
    class Meta:
        model = User

    email = fields.Email(required=True)


class ChangePasswordSchema(Schema):
    password = fields.String(required=True)
    new_password = fields.String(required=True, validate=password_validator)
    new_password_re = fields.String(required=True, validate=password_validator)

    @validates_schema
    def validate_equal(self, data: dict, **kwargs) -> None:
        if data['new_password'] != data['new_password_re']:
            raise ValidationError('new_password must be equal to new_password_re.')


class UserJWTPayloadSchema(ma.SQLAlchemySchema):
    """Represents a user data, included in JWT"""
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()


class LoginEntrieSchema(ma.SQLAlchemySchema):
    """Load-only schema for storing information about the login incident."""

    class Meta:
        model = LoginEntrie
        dump_only = ['id']

    user_id = ma.auto_field()
    user_agent = fields.Raw()
    remote_addr = fields.IP(required=True)

    @post_load
    def make_obj(self, data: dict, **kwargs) -> LoginEntrie:
        return LoginEntrie(
            user_id=data['user_id'],
            agent_platform=data['user_agent'].platform,
            agent_browser=data['user_agent'].browser,
            agent_version=data['user_agent'].version,
            agent_language=data['user_agent'].language,
            agent_string=data['user_agent'].string,
            remote_addr=data['remote_addr'].exploded
        )


class OutputEntrieSchema(ma.SQLAlchemyAutoSchema):
    """Represents LoginEntrie directly"""
    class Meta:
        model = LoginEntrie


class RoleSchema(ma.SQLAlchemySchema):
    """Role registration schema and getting standard data."""

    class Meta:
        model = Role
        dump_only = ['id']

    id = fields.UUID(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)

    @post_load
    def make_obj(self, data: dict, **kwargs) -> Role:
        return Role(**data)


class UpdateRoleSchema(ma.SQLAlchemySchema):
    """Schema for updating role."""
    class Meta:
        model = Role

    name = fields.String(required=False)
    description = fields.String(required=False)


class ProvidedRoleSchema(ma.SQLAlchemyAutoSchema):
    """Used to seting roles"""
    class Meta:
        model = Role
        dump_only = ['name', 'description']
