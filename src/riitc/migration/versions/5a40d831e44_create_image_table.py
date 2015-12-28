"""create image table

Revision ID: 5a40d831e44
Revises: 33e33f064c9f
Create Date: 2015-12-24 06:53:07.185295

"""

# revision identifiers, used by Alembic.
revision = '5a40d831e44'
down_revision = '33e33f064c9f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('image',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hashkey', sa.Unicode(length=2083), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_date_created'), 'image', ['date_created'], unique=False)
    op.alter_column(u'account', 'nickname',
                    existing_type=sa.VARCHAR(length=256),
                    nullable=False)
    op.create_unique_constraint(None, 'account', ['nickname'])
    op.create_index(op.f('ix_image_hashkey'),
                    'image', ['hashkey'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_image_hashkey'), table_name='image')
    op.drop_constraint(None, 'account')
    op.alter_column(u'account', 'nickname',
                    existing_type=sa.VARCHAR(length=256),
                    nullable=True)
    op.drop_index(op.f('ix_image_date_created'), table_name='image')
    op.drop_table('image')
