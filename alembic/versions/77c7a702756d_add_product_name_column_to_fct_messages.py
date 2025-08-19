"""add product_name column to fct_messages

Revision ID: 77c7a702756d
Revises: 83a2eeffdb5f
Create Date: 2025-08-18 22:04:44.006092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision = 'add_product_name_column'
down_revision = '83a2eeffdb5f'  # your init_schema revision
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        'fct_messages',
        sa.Column('product_name', sa.String(), nullable=True),
        schema='raw_analytics'
    )

def downgrade() -> None:
    op.drop_column('fct_messages', 'product_name', schema='raw_analytics')
