"""add executable column to software table

Revision ID: f1e4fcb38055
Revises: 5b2c3b8d2ff5
Create Date: 2021-10-28 10:52:17.495707

"""
from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = 'f1e4fcb38055'
down_revision = '5b2c3b8d2ff5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('software', Column('executable', String))


def downgrade():
    op.drop_column('software', 'executable')

