from marshmallow import (post_load,
                         fields,
                         ValidationError,
                         validates_schema)
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from werkzeug.security import generate_password_hash

from app.models import Role, AllowedDevice, SignInEntrie
from app.models import User
from app.validators import password_validator
from app import ma


class AutoHashed:
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
            data['password']
        )
        return User(**data)


class BasicUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ['id', 'created', 'modified']

    roles = fields.Nested('BasicRoleSchema', many=True, default=[])


class UserSchema(BasicUserSchema, AutoHashed):
    pass


class ProfileSchema(ma.SQLAlchemyAutoSchema, AutoHashed):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'roles']
        dump_only = ['id', 'roles']
        load_only = ['password']

    roles = fields.Nested('BasicRoleSchema', many=True, default=[])
    password = auto_field(validate=password_validator)

    @post_load
    def make_obj(self, data: dict, **kwargs) -> User:
        data['password'] = self.get_password_hash(
            data['password']
        )
        return User(**data)


class ChangePasswordSchema(SQLAlchemySchema):
    class Meta:
        model = User

    password = fields.String(required=True)
    new_password = fields.String(required=True, validate=password_validator)
    new_password_re = fields.String(required=True, validate=password_validator)

    @validates_schema
    def validate_equal(self, data: dict, **kwargs) -> None:
        if data['new_password'] != data['new_password_re']:
            raise ValidationError('new_password must be equal to new_password_re.')


class ChangeEmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('email',)


class SignInEntrieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SignInEntrie
        load_instance = True
        dump_only = ['id']
        fields = ('id', 'user_id', 'user_agent', 'remote_addr')


class AllowedDeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllowedDevice
        load_instance = True
        dump_only = ['id']
        fields = ('id', 'user_id', 'user_agent')


class BasicRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        dump_only = ['id', 'created', 'modified']


class RoleSchema(BasicRoleSchema):
    class Meta:
        model = Role
        dump_only = ['id']
        load_instance = True
