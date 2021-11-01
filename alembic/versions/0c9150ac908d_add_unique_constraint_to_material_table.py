"""add unique constraint to material table

Revision ID: 0c9150ac908d
Revises: d213d2faef0b
Create Date: 2021-10-28 10:11:49.393485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c9150ac908d'
down_revision = 'd213d2faef0b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_material_01', 'material', ['name', 'temperature'])


def downgrade():
    op.drop_constraint('uniq_material_01', 'material')
