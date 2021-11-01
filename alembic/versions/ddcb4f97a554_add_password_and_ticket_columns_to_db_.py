"""add password and ticket columns to db_user table

Revision ID: ddcb4f97a554
Revises: 98a3fbeaff6f
Create Date: 2021-10-28 09:57:31.436934

"""
from alembic import op
from sqlalchemy import Column, String, DateTime, Integer

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddcb4f97a554'
down_revision = '98a3fbeaff6f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('db_user', Column('password', String, nullable=False))
    op.add_column('db_user', Column('ticket_hash', String))
    op.add_column('db_user', Column('ticket_length', Integer, nullable=False))
    op.add_column('db_user', Column('ticket_timeout', DateTime, nullable=False))
    op.add_column('db_user', Column('access_level', Integer, nullable=False))


def downgrade():
    op.drop_column('db_user', 'password')
    op.drop_column('db_user', 'ticket_hash')
    op.drop_column('db_user', 'ticket_length')
    op.drop_column('db_user', 'ticket_timeout')
    op.drop_column('db_user', 'access_level')
