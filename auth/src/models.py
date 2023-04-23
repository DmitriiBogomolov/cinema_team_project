import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, Timestamp

from src import db


class User(db.Model, Timestamp):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'User (ID: <{self.id}>)'


class UserProfile(db.Model, Timestamp):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True, nullable=False)
