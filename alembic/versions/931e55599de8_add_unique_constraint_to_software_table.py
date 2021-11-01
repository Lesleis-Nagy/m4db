"""add unique constraint to software table

Revision ID: 931e55599de8
Revises: f1e4fcb38055
Create Date: 2021-10-28 10:54:15.305576

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '931e55599de8'
down_revision = 'f1e4fcb38055'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_software_01', 'software', ['name', 'version'])


def downgrade():
    op.drop_constraint('uniq_software_01', 'software')
