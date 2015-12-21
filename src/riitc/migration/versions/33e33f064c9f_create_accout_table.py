"""create accout table

Revision ID: 33e33f064c9f
Revises: 35a80b511eb7
Create Date: 2015-12-19 04:29:02.108568

"""

# revision identifiers, used by Alembic.
revision = '33e33f064c9f'
down_revision = '35a80b511eb7'

from alembic import op
import sqlalchemy as sa
from studio.core.sqla.types import JSONType


def upgrade():
    op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('account',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nickname', sa.Unicode(length=256), nullable=True),
        sa.Column('email', sa.Unicode(length=1024), nullable=True),
        sa.Column('is_email_confirmed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('info', JSONType(), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_date_created'), 'account', ['date_created'], unique=False)
    op.create_index(op.f('ix_account_email'), 'account', ['email'], unique=False)
    op.create_table('roles_accounts',
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], [u'account.id'], ),
    sa.ForeignKeyConstraint(['role_id'], [u'role.id'], )
    )
    op.alter_column(u'staff', 'name',
                    existing_type=sa.VARCHAR(length=256),
                    nullable=False)
    op.alter_column(u'staff', 'synopsis',
                    existing_type=sa.TEXT(),
                    nullable=False)


def downgrade():
    op.alter_column(u'staff', 'synopsis',
                    existing_type=sa.TEXT(),
                    nullable=True)
    op.alter_column(u'staff', 'name',
                    existing_type=sa.VARCHAR(length=256),
                    nullable=True)
    op.drop_table('roles_accounts')
    op.drop_index(op.f('ix_account_email'), table_name='account')
    op.drop_index(op.f('ix_account_date_created'), table_name='account')
    op.drop_table('account')
    op.drop_table('role')
