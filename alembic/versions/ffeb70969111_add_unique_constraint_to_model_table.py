"""add unique constraint to model table

Revision ID: ffeb70969111
Revises: 1274a9687df1
Create Date: 2021-10-28 10:25:49.416740

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'ffeb70969111'
down_revision = '1274a9687df1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_model_01', 'model', ['unique_id'])


def downgrade():
    op.drop_constraint('uniq_model_01', 'model')
