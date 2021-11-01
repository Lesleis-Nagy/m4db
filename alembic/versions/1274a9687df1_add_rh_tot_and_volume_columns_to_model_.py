"""add rh_tot and volume columns to model table

Revision ID: 1274a9687df1
Revises: 0c9150ac908d
Create Date: 2021-10-28 10:22:40.780924

"""
from alembic import op
from sqlalchemy import Column, Float


# revision identifiers, used by Alembic.
revision = '1274a9687df1'
down_revision = '0c9150ac908d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('model', Column('rh_tot', Float))
    op.add_column('model', Column('volume', Float))


def downgrade():
    op.drop_column('model', 'rh_tot')
    op.drop_column('model', 'volume')
