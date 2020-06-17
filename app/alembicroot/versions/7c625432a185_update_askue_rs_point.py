"""update askue_rs_point

Revision ID: 7c625432a185
Revises: 088e8baa95a7
Create Date: 2020-02-11 14:33:14.305270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c625432a185'
down_revision = '088e8baa95a7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('askue_rs_point', sa.Column('number_point', sa.Integer(), nullable=False))
    op.add_column('askue_rs_point', sa.Column('driver', sa.String(length=25), nullable=False))


def downgrade():
    op.drop_column('askue_rs_point', 'number_point')
    op.drop_column('askue_rs_point', 'driver')
