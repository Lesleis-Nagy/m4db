"""add unique constraint to physical_constant table

Revision ID: 07a8b226f9c5
Revises: e2ff5bce75e7
Create Date: 2021-10-28 10:41:16.942669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07a8b226f9c5'
down_revision = 'e2ff5bce75e7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_physical_constant_01', 'physical_constant', ['symbol'])


def downgrade():
    op.drop_constraint('uniq_physical_constant_01', 'physical_constant')
