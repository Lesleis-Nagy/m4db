"""add unique constraint to running_status table

Revision ID: 5b2c3b8d2ff5
Revises: e3fbca8cc141
Create Date: 2021-10-28 10:49:28.639269

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '5b2c3b8d2ff5'
down_revision = 'e3fbca8cc141'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_running_status_01', 'running_status', ['name'])


def downgrade():
    op.drop_constraint('uniq_running_status_01', 'running_status')
