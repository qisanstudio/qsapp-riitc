"""create_table

Revision ID: 35a80b511eb7
Revises: None
Create Date: 2015-11-07 12:42:25.318260

"""

# revision identifiers, used by Alembic.
revision = '35a80b511eb7'
down_revision = None

from alembic import op
import sqlalchemy as sa
from studio.core.sqla.types import JSONType


def upgrade():
    op.create_table('level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(length=256), nullable=True),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_level_date_created'), 'level', ['date_created'], unique=False)
    op.create_table('navi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_navi_date_created'), 'navi', ['date_created'], unique=False)
    op.create_index(op.f('ix_navi_name'), 'navi', ['name'], unique=True)
    op.create_table('channel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Unicode(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], [u'channel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channel_date_created'), 'channel', ['date_created'], unique=False)
    op.create_index(op.f('ix_channel_name'), 'channel', ['name'], unique=True)
    op.create_index(op.f('ix_channel_parent_id'), 'channel', ['parent_id'], unique=False)
    op.create_table('slide',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(length=256), nullable=True),
    sa.Column('describe', sa.Unicode(length=1024), nullable=True),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('image', sa.Unicode(length=2083), nullable=False),
    sa.Column('link', sa.Unicode(length=2083), nullable=True),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_slide_date_created'), 'slide', ['date_created'], unique=False)
    op.create_index(op.f('ix_slide_describe'), 'slide', ['describe'], unique=False)
    op.create_index(op.f('ix_slide_order'), 'slide', ['order'], unique=False)
    op.create_index(op.f('ix_slide_title'), 'slide', ['title'], unique=False)
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('is_sticky', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('title', sa.Unicode(length=64), nullable=False),
    sa.Column('date_published', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], [u'channel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_article_channel_id'), 'article', ['channel_id'], unique=False)
    op.create_index(op.f('ix_article_date_created'), 'article', ['date_created'], unique=False)
    op.create_index(op.f('ix_article_date_published'), 'article', ['date_published'], unique=False)
    op.create_index(op.f('ix_article_title'), 'article', ['title'], unique=True)
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=256), nullable=True),
    sa.Column('avatar', sa.Unicode(length=2083), nullable=False),
    sa.Column('synopsis', sa.UnicodeText(), nullable=True),
    sa.Column('info', JSONType(), nullable=True),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
    sa.ForeignKeyConstraint(['level_id'], [u'level.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_staff_date_created'), 'staff', ['date_created'], unique=False)
    op.create_index(op.f('ix_staff_level_id'), 'staff', ['level_id'], unique=False)
    op.create_table('navi_channel',
    sa.Column('navi_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], [u'channel.id'], ),
    sa.ForeignKeyConstraint(['navi_id'], [u'navi.id'], ),
    sa.PrimaryKeyConstraint('navi_id', 'channel_id')
    )
    op.create_index(op.f('ix_navi_channel_channel_id'), 'navi_channel', ['channel_id'], unique=False)
    op.create_index(op.f('ix_navi_channel_navi_id'), 'navi_channel', ['navi_id'], unique=False)
    op.create_table('channel_summary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['id'], [u'channel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['id'], [u'article.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('article_content')
    op.drop_table('channel_summary')
    op.drop_index(op.f('ix_navi_channel_navi_id'), table_name='navi_channel')
    op.drop_index(op.f('ix_navi_channel_channel_id'), table_name='navi_channel')
    op.drop_table('navi_channel')
    op.drop_index(op.f('ix_staff_level_id'), table_name='staff')
    op.drop_index(op.f('ix_staff_date_created'), table_name='staff')
    op.drop_table('staff')
    op.drop_index(op.f('ix_article_title'), table_name='article')
    op.drop_index(op.f('ix_article_date_published'), table_name='article')
    op.drop_index(op.f('ix_article_date_created'), table_name='article')
    op.drop_index(op.f('ix_article_channel_id'), table_name='article')
    op.drop_table('article')
    op.drop_index(op.f('ix_slide_title'), table_name='slide')
    op.drop_index(op.f('ix_slide_order'), table_name='slide')
    op.drop_index(op.f('ix_slide_describe'), table_name='slide')
    op.drop_index(op.f('ix_slide_date_created'), table_name='slide')
    op.drop_table('slide')
    op.drop_index(op.f('ix_channel_parent_id'), table_name='channel')
    op.drop_index(op.f('ix_channel_name'), table_name='channel')
    op.drop_index(op.f('ix_channel_date_created'), table_name='channel')
    op.drop_table('channel')
    op.drop_index(op.f('ix_navi_name'), table_name='navi')
    op.drop_index(op.f('ix_navi_date_created'), table_name='navi')
    op.drop_table('navi')
    op.drop_index(op.f('ix_level_date_created'), table_name='level')
    op.drop_table('level')
