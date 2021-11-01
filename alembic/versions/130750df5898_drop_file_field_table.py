"""drop file_field table

Revision ID: 130750df5898
Revises: 8aaa7e46f987
Create Date: 2021-10-27 21:56:16.025079

"""
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from alembic import op

# revision identifiers, used by Alembic.
revision = '130750df5898'
down_revision = '8aaa7e46f987'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('file_field')


def downgrade():
    now = datetime.now

    op.create_table(
        'file_field',
        Column('id', Integer, primary_key=True, nullable=False),
        Column('last_modified', DateTime, default=now, onupdate=now, nullable=False),
        Column('created', DateTime, default=now, nullable=False)
    )
