"""Initial migration.

Revision ID: eed172063a86
Revises:
Create Date: 2023-06-17 20:12:16.930076

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'eed172063a86'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
    sa.Column('password', sa.String(length=300), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_confirm', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('otp_secret', sa.String(length=32), nullable=True),
    sa.Column('is_two_auth', sa.Boolean(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('allowed_devices',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('sign_in_entries',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('remote_addr', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'created'),
    postgresql_partition_by='RANGE (created)'
    )
    op.create_table('social_account',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('social_id', sa.Text(), nullable=False),
    sa.Column('social_name', sa.Text(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_pk')
    )
    op.create_table('user_roles',
    sa.Column('left_id', sa.UUID(), nullable=True),
    sa.Column('right_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['left_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['right_id'], ['roles.id'], ondelete='CASCADE')
    )
    op.create_table('sign_in_entries_2023',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('remote_addr', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'created')
    )
    op.create_table('sign_in_entries_2024',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('remote_addr', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'created')
    )
    # ### end Alembic commands ###
    op.execute("""ALTER TABLE sign_in_entries ATTACH PARTITION sign_in_entries_2023
                FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');""")

    op.execute("""ALTER TABLE sign_in_entries ATTACH PARTITION sign_in_entries_2024
                    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');""")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sign_in_entries_2024')
    op.drop_table('sign_in_entries_2023')
    op.drop_table('user_roles')
    op.drop_table('social_account')
    op.drop_table('sign_in_entries')
    op.drop_table('allowed_devices')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
