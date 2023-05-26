from marshmallow import post_load, fields
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
    @post_load
    def make_obj(self, data: dict, **kwargs) -> User:
        data['password'] = generate_password_hash(
            password=data['password'],
            method='pbkdf2:sha512',
            salt_length=16
        )
        return User(**data)

    def verify_hash(self, pwhash: str, password: str) -> bool:
        return check_password_hash(pwhash, password)
