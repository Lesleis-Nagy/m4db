"""add unique constraint to anisotropy_form table

Revision ID: 977eda6841ef
Revises: 828724d4ee52
Create Date: 2021-10-28 09:47:48.975435

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '977eda6841ef'
down_revision = '828724d4ee52'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_anisotropy_form_01', 'anisotropy_form', ['name'])


def downgrade():
    op.drop_constraint('uniq_anisotropy_form_01', 'anisotropy_form')
