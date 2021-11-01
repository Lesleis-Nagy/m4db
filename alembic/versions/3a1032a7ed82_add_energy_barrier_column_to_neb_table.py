"""add energy_barrier column to neb table

Revision ID: 3a1032a7ed82
Revises: ffeb70969111
Create Date: 2021-10-28 10:31:39.491673

"""
from alembic import op
from sqlalchemy import Column, Float

# revision identifiers, used by Alembic.
revision = '3a1032a7ed82'
down_revision = 'ffeb70969111'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('neb', Column('energy_barrier', Float))


def downgrade():
    op.drop_column('neb', 'energy_barrier')
