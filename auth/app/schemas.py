from marshmallow import post_load

from app.models import Role
from app import ma


class RoleSchema(ma.SQLAlchemyAutoSchema):
    """Just testing"""
    class Meta:
        model = Role
        dump_only = ['id']

    @post_load
    def make_obj(self, data: dict, **kwargs) -> Role:
        return Role(**data)
