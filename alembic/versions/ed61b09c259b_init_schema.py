"""init schema

Revision ID: ed61b09c259b
Revises: 
Create Date: 2025-08-18 20:36:46.339634

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ed61b09c259b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # dim_channels with sequence
    op.execute("CREATE SEQUENCE raw_analytics.dim_channels_channel_key_seq")
    op.create_table(
        'dim_channels',
        sa.Column('channel_key', sa.Integer(), server_default=sa.text("nextval('raw_analytics.dim_channels_channel_key_seq')"), primary_key=True, nullable=False),
        sa.Column('channel_name', sa.String(), nullable=False, unique=True),
        sa.Column('channel_type', sa.String(), nullable=True),
        schema='raw_analytics'
    )
    op.create_index('ix_dim_channels_channel_key', 'dim_channels', ['channel_key'], unique=False, schema='raw_analytics')

    # dim_dates with sequence
    op.execute("CREATE SEQUENCE raw_analytics.dim_dates_date_id_seq")
    op.create_table(
        'dim_dates',
        sa.Column('date_id', sa.Integer(), server_default=sa.text("nextval('raw_analytics.dim_dates_date_id_seq')"), primary_key=True, nullable=False),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('month', sa.Integer(), nullable=True),
        sa.Column('day', sa.Integer(), nullable=True),
        sa.Column('weekday', sa.String(), nullable=True),
        sa.Column('week', sa.Integer(), nullable=True),
        schema='raw_analytics'
    )

    # fct_messages with sequence
    op.execute("CREATE SEQUENCE raw_analytics.fct_messages_message_id_seq")
    op.create_table(
        'fct_messages',
        sa.Column('message_id', sa.Integer(), server_default=sa.text("nextval('raw_analytics.fct_messages_message_id_seq')"), primary_key=True, nullable=False),
        sa.Column('channel_key', sa.Integer(), sa.ForeignKey('raw_analytics.dim_channels.channel_key'), nullable=True),
        sa.Column('date_id', sa.Integer(), sa.ForeignKey('raw_analytics.dim_dates.date_id'), nullable=True),
        sa.Column('message_text', sa.Text(), nullable=True),
        sa.Column('message_length', sa.Integer(), nullable=True),
        sa.Column('has_image', sa.Boolean(), nullable=True),
        sa.Column('product_name', sa.String(), nullable=True),
        schema='raw_analytics'
    )
    op.create_index('ix_fct_messages_message_id', 'fct_messages', ['message_id'], unique=False, schema='raw_analytics')

    # fct_image_detections with sequence
    op.execute("CREATE SEQUENCE raw.fct_image_detections_detection_id_seq")
    op.create_table(
        'fct_image_detections',
        sa.Column('detection_id', sa.Integer(), server_default=sa.text("nextval('raw.fct_image_detections_detection_id_seq')"), primary_key=True, nullable=False),
        sa.Column('message_id', sa.Integer(), sa.ForeignKey('raw_analytics.fct_messages.message_id'), nullable=True),
        sa.Column('detected_object_class', sa.String(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        schema='raw'
    )
    op.create_index('ix_fct_image_detections_detection_id', 'fct_image_detections', ['detection_id'], unique=False, schema='raw')


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index('ix_fct_image_detections_detection_id', table_name='fct_image_detections', schema='raw')
    op.drop_table('fct_image_detections', schema='raw')
    op.execute("DROP SEQUENCE IF EXISTS raw.fct_image_detections_detection_id_seq")

    op.drop_index('ix_fct_messages_message_id', table_name='fct_messages', schema='raw_analytics')
    op.drop_table('fct_messages', schema='raw_analytics')
    op.execute("DROP SEQUENCE IF EXISTS raw_analytics.fct_messages_message_id_seq")

    op.drop_table('dim_dates', schema='raw_analytics')
    op.execute("DROP SEQUENCE IF EXISTS raw_analytics.dim_dates_date_id_seq")

    op.drop_index('ix_dim_channels_channel_key', table_name='dim_channels', schema='raw_analytics')
    op.drop_table('dim_channels', schema='raw_analytics')
    op.execute("DROP SEQUENCE IF EXISTS raw_analytics.dim_channels_channel_key_seq")
