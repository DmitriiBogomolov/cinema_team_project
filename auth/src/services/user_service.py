from uuid import UUID
from http import HTTPStatus
from flask import abort
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from src.schemas import UserSchema, LoginEntrieSchema, UpdateUserSchema
from src.models import User, LoginEntrie
from src.exceptions import AlreadyExistsError
from app import db


user_schema = UserSchema()
entrie_schema = LoginEntrieSchema()  # repr one record of logins history
update_schema = UpdateUserSchema()


class UserService():
    def create_user(self, user_data: dict) -> User:
        """Create new user"""
        user = user_schema.load(user_data)

        if User.query.filter_by(email=user.email).first():
            raise AlreadyExistsError('User with that email already exists.')

        db.session.add(user)
        db.session.commit()

        return user

    def update_user(self, cur_user: User, user_data: dict) -> User:
        """Update provided user data"""
        valid_data = update_schema.load(user_data)

        try:
            User.query.filter_by(id=cur_user.id).update(valid_data)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise AlreadyExistsError('Role with that name already exists')

        return cur_user

    def change_password(self, user: User, old_pass: str, new_pass: str) -> None:
        """Change password if cur_password is valid"""
        if not check_password_hash(user.password, old_pass):
            abort(HTTPStatus.UNAUTHORIZED)

        user.password = UserSchema.get_password_hash(new_pass)
        db.session.commit()

    def save_entrie_log(self, user_id: UUID, request) -> None:
        """Save a record to user log-in history"""
        entrie = entrie_schema.load({
            'user_id': user_id,
            'user_agent': request.user_agent,
            'remote_addr': request.environ['REMOTE_ADDR']
        })
        db.session.add(entrie)
        db.session.commit()

    def get_entrie_log(self,
                       user_id: UUID,
                       page: int,
                       per_page: int
                       ) -> list[LoginEntrie]:
        """Get user log-in history"""
        return LoginEntrie.query.filter_by(user_id=user_id) \
            .order_by(LoginEntrie.created.desc()) \
            .paginate(page=page, per_page=per_page, error_out=True)


user_service = UserService()
