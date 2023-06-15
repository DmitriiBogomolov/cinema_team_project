from sqlalchemy import and_
from marshmallow import (post_load,
                         fields,
                         ValidationError,
                         validates_schema)
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from werkzeug.security import generate_password_hash

from app.models import Role, AllowedDevice, SignInEntrie
from app.models import User, SocialAccount
from app.helpers.validators import password_validator
from app.core.extensions import ma


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
        load_only = ['password', 'otp_secret']
        dump_only = ['id', 'created', 'modified']

    roles = fields.Nested('BasicRoleSchema', many=True, default=[])


class UserSchema(BasicUserSchema, AutoHashed):
    pass


class ProfileSchema(ma.SQLAlchemyAutoSchema, AutoHashed):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'roles', 'is_active']
        dump_only = ['id', 'roles', 'is_active']
        load_only = ['password']

    roles = fields.Nested('ProfileRoleSchema', many=True, default=[])
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
        fields = ('id', 'user_id', 'user_agent', 'remote_addr', 'created')


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


class ProfileRoleSchema(BasicRoleSchema):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class RoleSchema(BasicRoleSchema):
    class Meta:
        model = Role
        dump_only = ['id']
        load_instance = True


class SocialAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SocialAccount
        load_instance = True
        dump_only = ['id']
        fields = ('id', 'user_id', 'social_id', 'social_name')

    @classmethod
    def is_account_exists(cls, social_id: str, social_name: str):
        account = (
            SocialAccount.query
            .filter(
                and_(
                    SocialAccount.social_id == social_id,
                    SocialAccount.social_name == social_name
                )
            )
            .first()
        )
        return bool(account)


class AddOtpSecretSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('otp_secret', 'is_two_auth')
