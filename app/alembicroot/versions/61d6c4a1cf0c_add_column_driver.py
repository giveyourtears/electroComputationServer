"""add column driver

Revision ID: 61d6c4a1cf0c
Revises: 2cbc63255b58
Create Date: 2020-03-12 12:10:27.963976

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '61d6c4a1cf0c'
down_revision = '2cbc63255b58'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('calc_balance', sa.Column('driver', sa.String(length=50), nullable=True))


def downgrade():
   op.drop_column('calc_balance', 'driver')
