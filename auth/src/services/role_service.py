from src.schemas import RoleSchema, LoginEntrieSchema, UpdateRoleSchema
from src.models import Role
from app import db


role_schema = RoleSchema()
entrie_schema = LoginEntrieSchema()  # repr one record of logins history
update_schema = UpdateRoleSchema()


class AlreadyExistsError(Exception):
    """Called if the role already exist"""
    pass


class RoleService():
    def create_role(self, role_data: dict) -> Role:
        """Create new role"""
        role = role_schema.load(role_data)

        if role.query.filter_by(name=role.name).first():
            raise AlreadyExistsError

        db.session.add(role)
        db.session.commit()

        return role

    def update_role(self, cur_role: Role, role_data: dict) -> Role:
        """Update provided role data"""
        valid_data = update_schema.load(role_data)

        if Role.query.filter_by(name=valid_data['name']).first():
            raise AlreadyExistsError

        cur_role.email = valid_data['name']
        db.session.commit()

        return cur_role

    def delete_role(self, role_data: dict) -> Role:
        """Removes the role"""
        role = role_schema.load(role_data)

        if role.query.filter_by(name=role.name).first():
            raise AlreadyExistsError

        db.session.delete(role)
        db.session.commit()

        return role


role_service = RoleService()
