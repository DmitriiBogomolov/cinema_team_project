from sqlalchemy import (
    Column, String, CheckConstraint, Time,
    ForeignKey, Date
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import ARRAY


SqlalchemyBase = declarative_base()  # Точка входа в sqlalchemy


class StoredEvent(SqlalchemyBase):
    """Хранимое событие (sqlalchemy + postgresql)"""
    __tablename__ = 'events'

    name = Column(String(20), primary_key=True)
    description = Column(String(50))

    #  если событие периодическое - следующие поля заполняются
    days = Column(ARRAY(String(2)))  # массив дней от 0 до 7
    weeks = Column(ARRAY(String(2)))  # массив недель от 0 до 3
    months = Column(ARRAY(String(2)))  # массив месяцев от 0 до 11
    send_time = Column(Time(timezone=False))
    last_generated = Column(Date)

    email_template = relationship('EmailTemlate', uselist=False, back_populates='event')

    __table_args__ = (
        CheckConstraint('array_length(days, 1) > 0', name='days_not_empty'),
        CheckConstraint('array_length(days, 1) < 7', name='days_max_length'),
        CheckConstraint('array_length(weeks, 1) > 0', name='weeks_not_empty'),
        CheckConstraint('array_length(weeks, 1) < 4', name='weeks_max_length'),
        CheckConstraint('array_length(months, 1) > 0', name='months_not_empty'),
        CheckConstraint('array_length(months, 1) < 12', name='months_max_length'),
    )

    def __str__(self):
        return self.name


class EmailTemlate(SqlalchemyBase):
    """Хранимые шаблоны уведомлений (sqlalchemy + postgresql)"""
    __tablename__ = 'email_templates'

    event_name = Column(String(20), ForeignKey('events.name'), primary_key=True)
    topic_message = Column(String(50), nullable=False)
    template = Column(String(120), nullable=False)

    event = relationship(
        'StoredEvent',
        back_populates='email_template',
        primaryjoin='EmailTemlate.event_name == StoredEvent.name'
    )
