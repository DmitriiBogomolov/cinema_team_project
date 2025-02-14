"""create database

Revision ID: fa228e9d9903
Revises:
Create Date: 2023-10-13 14:20:18.076209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa228e9d9903'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'events',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('days', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('weeks', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('months', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('send_time', sa.Time(), nullable=True),
        sa.Column('last_generated', sa.Date(), nullable=True),
        sa.CheckConstraint('array_length(days, 1) < 7', name='days_max_length'),
        sa.CheckConstraint('array_length(days, 1) > 0', name='days_not_empty'),
        sa.CheckConstraint('array_length(months, 1) < 12', name='months_max_length'),
        sa.CheckConstraint('array_length(months, 1) > 0', name='months_not_empty'),
        sa.CheckConstraint('array_length(weeks, 1) < 4', name='weeks_max_length'),
        sa.CheckConstraint('array_length(weeks, 1) > 0', name='weeks_not_empty'),
        sa.PrimaryKeyConstraint('name')
    )
    op.create_table(
        'email_templates',
        sa.Column('event_name', sa.String(), nullable=False),
        sa.Column('topic_message', sa.String(), nullable=False),
        sa.Column('template', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['event_name'], ['events.name'], ),
        sa.PrimaryKeyConstraint('event_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_templates')
    op.drop_table('events')
    # ### end Alembic commands ###
