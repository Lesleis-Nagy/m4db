"""add unique constraint to unit table

Revision ID: 1ca450ab05de
Revises: 931e55599de8
Create Date: 2021-10-28 10:56:02.599531

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '1ca450ab05de'
down_revision = '931e55599de8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_unit_01', 'unit', ['symbol'])


def downgrade():
    op.drop_constraint('uniq_unit_01', 'unit')
