"""add unique constraints to geometry table

Revision ID: d213d2faef0b
Revises: ddcb4f97a554
Create Date: 2021-10-28 10:06:59.244305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd213d2faef0b'
down_revision = 'ddcb4f97a554'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_geometry_01', 'geometry', ['name', 'size', 'size_unit_id'])
    op.create_unique_constraint('uniq_geometry_02', 'geometry', ['unique_id'])


def downgrade():
    op.drop_constraint('uniq_geometry_01', 'geometry')
    op.drop_constraint('uniq_geometry_02', 'geometry')
