import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy import PrimaryKeyConstraint, event, DDL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType, Timestamp

from app.core.extensions import db


user_role = db.Table(
    'user_roles',
    db.Column('left_id', db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('right_id', db.ForeignKey('roles.id', ondelete='CASCADE')),
)


class BasicModel(Timestamp):
    """Provide standard fields and methods"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    @classmethod
    def get_by_id(model, id: uuid) -> db.Model:
        return db.get_or_404(model, id)

    @classmethod
    def get_list(model) -> list[db.Model]:
        return db.session.query(model).all()

    def update(self, data: dict) -> db.Model:
        try:
            db.session.query(self.__class__).filter_by(id=self.id).update(data)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e
        return self

    def save(self) -> db.Model:
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()


class Role(db.Model, BasicModel):
    """Represents users role"""
    __tablename__ = 'roles'

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)


class SignInMixin:
    """Represents a record of user log-ins journal"""
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)
    remote_addr = db.Column(db.String(100), nullable=False)


class SignInEntrie(SignInMixin, db.Model, BasicModel):
    __tablename__ = 'sign_in_entries'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'created'),
        {
            'postgresql_partition_by': 'RANGE (created)',
        }
    )


class SignInEntrie2023(SignInMixin, db.Model, BasicModel):
    __tablename__ = 'sign_in_entries_2023'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'created'),
    )


class SignInEntrie2024(SignInMixin, db.Model, BasicModel):
    __tablename__ = 'sign_in_entries_2024'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'created'),
    )


SignInEntrie2023.__table__.add_is_dependent_on(SignInEntrie.__table__)
SignInEntrie2024.__table__.add_is_dependent_on(SignInEntrie.__table__)
event.listen(
    SignInEntrie2023.__table__,
    'after_create',
    DDL("""ALTER TABLE sign_in_entries ATTACH PARTITION sign_in_entries_2023
           FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');""")
)
event.listen(
    SignInEntrie2024.__table__,
    'after_create',
    DDL("""ALTER TABLE sign_in_entries ATTACH PARTITION sign_in_entries_2024
           FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');""")
)


class AllowedDevice(db.Model, BasicModel):
    """Represents a record of user log-ins journal"""
    __tablename__ = 'allowed_devices'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)


class SocialAccount(db.Model, BasicModel):
    """Represents social account"""
    __tablename__ = 'social_account'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'), )


class User(db.Model, BasicModel):
    """Represents user"""
    __tablename__ = 'users'

    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_confirm = db.Column(db.Boolean, nullable=False, default=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    otp_secret = db.Column(db.String(32))
    is_two_auth = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.relationship(
        'Role',
        secondary=user_role,
        backref='users'
    )
    sign_in_entries = db.relationship(
        'SignInEntrie',
        backref='sing_in_entries'
    )
    allowed_devices = db.relationship(
        'AllowedDevice',
        backref='allowed_devices'
    )
    social_account = db.relationship(
        'SocialAccount',
        backref='social_accounts'
    )

    @classmethod
    def get_by_email(cls, email: str):
        return User.query.filter_by(email=email).first()
