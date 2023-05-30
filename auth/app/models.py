import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, Timestamp

from app.extensions import db


user_role = db.Table(
    'user_roles',
    db.Column('left_id', db.ForeignKey('users.id')),
    db.Column('right_id', db.ForeignKey('roles.id')),
)


class BasicModel(Timestamp):
    """Provide standard fields and methods"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    @classmethod
    def get_by_id(model, id: uuid) -> object:
        return db.get_or_404(model, id)

    @classmethod
    def get_list(model) -> object:
        return db.session.query(model).all()

    def update(self, data: dict) -> object:
        try:
            db.session.query(self.__class__).filter_by(id=self.id).update(data)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e
        return self

    def save(self) -> object:
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e
        return self

    def delete(self) -> object:
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BasicModel):
    """Represents user"""
    __tablename__ = 'users'

    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.relationship(
        'Role',
        secondary=user_role,
        backref='users',
        cascade='all'
    )
    sign_in_entries = db.relationship(
        'SignInEntrie',
        backref='sing_in_entries'
    )
    allowed_devices = db.relationship(
        'AllowedDevice',
        backref='allowed_devices'
    )


class Role(db.Model, BasicModel):
    """Represents users role"""
    __tablename__ = 'roles'

    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)


class SignInEntrie(db.Model, BasicModel):
    """Represents a record of user log-ins journal"""
    __tablename__ = 'sign_in_entries'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    remote_addr = db.Column(db.String, nullable=False)


class AllowedDevice(db.Model, BasicModel):
    """Represents a record of user log-ins journal"""
    __tablename__ = 'allowed_devices'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
