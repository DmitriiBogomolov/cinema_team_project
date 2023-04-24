import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, Timestamp

from app import db


class BasicModel(Timestamp):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class User(db.Model, BasicModel):
    __tablename__ = 'users'

    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Session(db.Model, BasicModel):
    __tablename__ = 'sessions'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    agent_platform = db.Column(db.String)
    agent_browser = db.Column(db.String)
    agent_version = db.Column(db.String)
    agent_language = db.Column(db.String)
    agent_string = db.Column(db.String, nullable=False)
    remote_addr = db.Column(db.String, nullable=False)


class Role(db.Model, BasicModel):
    __tablename__ = 'roles'

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
