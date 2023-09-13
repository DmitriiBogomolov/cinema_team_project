import uuid
from sqlalchemy_utils import Timestamp
from sqlalchemy.dialects.postgresql import UUID, INTEGER, VARCHAR, TEXT
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BasicModel(Timestamp):
    """Provide standard fields and methods"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class Event(db.Model, BasicModel):
    """Represents user"""
    __tablename__ = 'evet_type'

    event_name = db.Column(VARCHAR(20), nullable=False)
    template = db.Column(TEXT, nullable=False)
    condition = db.Column(INTEGER, nullable=False)
