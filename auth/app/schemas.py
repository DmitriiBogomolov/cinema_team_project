from marshmallow import (post_load,
                         fields,
                         ValidationError,
                         validates_schema)
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import Role
from app.models import User
from app import ma


class BasicRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        dump_only = ['id']


class RoleSchema(BasicRoleSchema):
    @post_load
    def make_obj(self, data: dict, **kwargs) -> Role:
        return Role(**data)


class BasicUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ['id']

    roles = fields.Nested(BasicRoleSchema, many=True, default=[])


class UserSchema(BasicUserSchema):
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return generate_password_hash(
            password=password,
            method='pbkdf2:sha512',
            salt_length=16
        )

    @post_load
    def make_obj(self, data: dict, **kwargs) -> User:
        data['password'] = self.get_password_hash(
            super(),
            data['password']
        )
        return User(**data)

    def verify_hash(self, pwhash: str, password: str) -> bool:
        return check_password_hash(pwhash, password)


class ProfileSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        dump_only = ['id', 'roles']
        load_only = ['password']

    id = auto_field()
    email = auto_field()
    password = auto_field()
    roles = auto_field()


class ChangePasswordSchema(SQLAlchemySchema):
    class Meta:
        model = User

    password = fields.String(required=True)
    new_password = fields.String(required=True)
    new_password_re = fields.String(required=True)

    @validates_schema
    def validate_equal(self, data: dict, **kwargs) -> None:
        if data['new_password'] != data['new_password_re']:
            raise ValidationError('new_password must be equal to new_password_re.')


class ChangeEmailSchema(SQLAlchemySchema):
    class Meta:
        model = User

    email = auto_field()


class SingInEntrieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        dump_only = ['id']


class AllowedDeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        dump_only = ['id']
