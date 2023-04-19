import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType
from auth.db.postgres import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'
