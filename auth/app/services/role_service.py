from app.extensions import db
from app.models import Role
from app.schemas import RoleSchema


role_schema = RoleSchema()


class RoleService():
    """СУГУБО ТЕСТОВЫЙ СЕРВИС"""

    def get_roles(self) -> list[Role]:
        return db.session.query(Role).all()

    def create_role(self, role_data: dict) -> Role:
        role = role_schema.load(role_data)

        db.session.add(role)
        db.session.commit()

        return role


role_service = RoleService()
