import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, Timestamp


db = SQLAlchemy()


user_role = db.Table(
    'user_roles',
    db.Column('left_id', db.ForeignKey('users.id')),
    db.Column('right_id', db.ForeignKey('roles.id')),
)


class BasicModel(Timestamp):
    """Provide standard field: id, created, modified"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class User(db.Model, BasicModel):
    """Represents user"""
    __tablename__ = 'users'

    email = db.Column(EmailType, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False)
    roles = db.relationship(
        'Role',
        secondary=user_role,
        backref='users',
        cascade='all'
    )


class Role(db.Model, BasicModel):
    """Represents users role"""
    __tablename__ = 'roles'

    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)


class SingInEntrie(db.Model, BasicModel):
    """Represents a record of user log-ins journal"""
    __tablename__ = 'sign_in_enries'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    remote_addr = db.Column(db.String, nullable=False)


class AllowedDevice(db.Model, BasicModel):
    """Represents a record of user log-ins journal"""
    __tablename__ = 'allowed_devices'

    user_agent = db.Column(db.String, nullable=False)
