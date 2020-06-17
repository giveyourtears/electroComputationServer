"""update table country

Revision ID: 2cbc63255b58
Revises: 7c625432a185
Create Date: 2020-03-11 08:38:40.354841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2cbc63255b58'
down_revision = '7c625432a185'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('calc_balance', sa.Column('country', sa.String(), nullable=True))
    op.add_column('askue_rs_point', sa.Column('country', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    op.drop_column('calc_balance', 'country')
    op.drop_column('askue_rs_point', 'country')
