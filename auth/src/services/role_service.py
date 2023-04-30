from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.schemas import RoleSchema, LoginEntrieSchema, UpdateRoleSchema
from src.models import Role, User
from src.exceptions import AlreadyExistsError
from app import db


role_schema = RoleSchema()
entrie_schema = LoginEntrieSchema()  # repr one record of logins history
update_schema = UpdateRoleSchema()


class RoleService():
    def get_roles(self) -> list[Role]:
        return db.session.query(Role).all()

    def create_role(self, role_data: dict) -> Role:
        """Create new role"""
        role = role_schema.load(role_data)

        if Role.query.filter_by(name=role.name).first():
            raise AlreadyExistsError('Role already exists.')

        db.session.add(role)
        db.session.commit()

        return role

    def update_role(self, role_id: UUID, role_data: dict) -> Role:
        """Update provided role data"""
        valid_data = update_schema.load(role_data)
        role = db.get_or_404(Role, role_id)

        try:
            Role.query.filter_by(id=role_id).update(valid_data)
            db.session.commit()
        except IntegrityError:
            db.session.rollback
            raise AlreadyExistsError('Role with that name already exists')

        return role

    def delete_role(self, role_id: UUID) -> Role:
        """Removes the role"""
        role = db.get_or_404(Role, role_id)

        db.session.delete(role)
        db.session.commit()

        return role

    def set_roles(self, user_id: UUID, role_ids: list[UUID]) -> User:
        """Set roles for provided user"""
        user = db.get_or_404(User, user_id)
        roles = Role.query.filter(Role.id.in_(role_ids)).all()

        for role in roles:
            user.roles.append(role)

        db.session.commit()

        return user

    def revoke_roles(self, user_id: UUID, role_ids: list[UUID]) -> User:
        """Revoke roles from provided user"""
        user = db.get_or_404(User, user_id)
        roles = Role.query.filter(Role.id.in_(role_ids)).all()

        for role in roles:
            if role in user.roles:
                user.roles.remove(role)

        db.session.commit()

        return user


role_service = RoleService()
