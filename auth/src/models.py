import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, Timestamp


db = SQLAlchemy()


class BasicModel(Timestamp):
    """Provide standard field: id, created, modified"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class User(db.Model, BasicModel):
    """Represents user"""
    __tablename__ = 'users'

    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class LoginEntrie(db.Model, BasicModel):
    """Represents a record of user log-ins journal"""
    __tablename__ = 'login_entries'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    agent_platform = db.Column(db.String)
    agent_browser = db.Column(db.String)
    agent_version = db.Column(db.String)
    agent_language = db.Column(db.String)
    agent_string = db.Column(db.String, nullable=False)
    remote_addr = db.Column(db.String, nullable=False)


class Role(db.Model, BasicModel):
    """Represents users role"""
    __tablename__ = 'roles'

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
