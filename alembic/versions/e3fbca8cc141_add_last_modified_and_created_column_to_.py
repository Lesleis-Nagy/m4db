"""add last_modified and created column to project table

Revision ID: e3fbca8cc141
Revises: 07a8b226f9c5
Create Date: 2021-10-28 10:43:59.809902

"""
from datetime import datetime
from alembic import op
from sqlalchemy import Column, DateTime

# revision identifiers, used by Alembic.
revision = 'e3fbca8cc141'
down_revision = '07a8b226f9c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('project', Column('last_modified', DateTime, nullable=False, default=datetime.now))
    op.add_column('project', Column('created', DateTime, nullable=False, default=datetime.now))


def downgrade():
    op.drop_column('project', 'last_modified')
    op.drop_column('project', 'created')

