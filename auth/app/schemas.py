from marshmallow import post_load, fields
from werkzeug.security import generate_password_hash

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
    def hash_password(self, data: dict, **kwargs):
        data['password'] = generate_password_hash(data['password'], 'sha256')
        return data

    @post_load
    def make_obj(self, data: dict, **kwargs) -> User:
        return User(**data)
