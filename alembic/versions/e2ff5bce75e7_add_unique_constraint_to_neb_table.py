"""add unique constraint to neb table

Revision ID: e2ff5bce75e7
Revises: 3a1032a7ed82
Create Date: 2021-10-28 10:33:14.033992

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'e2ff5bce75e7'
down_revision = '3a1032a7ed82'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_neb_01', 'neb', ['unique_id'])


def downgrade():
    op.drop_constraint('uniq_neb_01', 'neb')
