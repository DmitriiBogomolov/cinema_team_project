"""create social_account table

Revision ID: af673f2722a0
Revises: 70e34d07272f
Create Date: 2023-06-07 16:32:04.797150

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'af673f2722a0'
down_revision = '70e34d07272f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('social_account',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('social_id', sa.Text(), nullable=False),
    sa.Column('social_name', sa.Text(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_pk')
    )


def downgrade():
    op.drop_table('social_account')
