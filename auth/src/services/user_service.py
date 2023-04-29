from uuid import UUID

from flask import abort
from werkzeug.security import check_password_hash

from src.schemas import UserSchema, LoginEntrieSchema, UpdateUserSchema
from src.models import User, LoginEntrie
from app import db


user_schema = UserSchema()
entrie_schema = LoginEntrieSchema()  # repr one record of logins history
update_schema = UpdateUserSchema()


class AlreadyExistsError(Exception):
    """Called if the user already exist"""
    pass


class UserService():
    def create_user(self, user_data: dict) -> User:
        """Create new user"""
        user = user_schema.load(user_data)

        if User.query.filter_by(email=user.email).first():
            raise AlreadyExistsError

        db.session.add(user)
        db.session.commit()

        return user

    def update_user(self, cur_user: User, user_data: dict) -> User:
        """Update provided user data"""
        valid_data = update_schema.load(user_data)

        if User.query.filter_by(email=valid_data['email']).first():
            raise AlreadyExistsError

        cur_user.email = valid_data['email']
        db.session.commit()

        return cur_user

    def change_password(self, user: User, old_pass: str, new_pass: str) -> None:
        """Change password if cur_password is valid"""
        if not check_password_hash(user.password, old_pass):
            abort(401)

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

    def get_entrie_log(self, user_id: UUID) -> list[LoginEntrie]:
        """Get user log-in history"""
        return (LoginEntrie.query.filter_by(user_id=user_id)
                                 .order_by(LoginEntrie.created.desc()))


user_service = UserService()
