"""drop mgst_start_end_pair_count table

Revision ID: 828724d4ee52
Revises: 130750df5898
Create Date: 2021-10-27 21:59:53.990770

"""
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String

from alembic import op

# revision identifiers, used by Alembic.
revision = '828724d4ee52'
down_revision = '130750df5898'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('mgst_start_end_pair_count')


def downgrade():
    now = datetime.now

    op.create_table(
        'mgst_start_end_pair_count',
        Column('id', Integer, primary_key=True, nullable=False),
        Column('material', String, nullable=False),
        Column('geometry', String, nullable=False),
        Column('size', String, nullable=False),
        Column('temperature', String, nullable=False),
        Column('pair_count', Integer, nullable=False, default=0),
        Column('last_modified', DateTime, default=now, onupdate=now, nullable=False),
        Column('created', DateTime, default=now, nullable=False)
    )
