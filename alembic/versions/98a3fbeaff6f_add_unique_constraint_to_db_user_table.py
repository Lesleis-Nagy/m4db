"""add unique constraint to db_user table

Revision ID: 98a3fbeaff6f
Revises: 977eda6841ef
Create Date: 2021-10-28 09:53:11.431293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98a3fbeaff6f'
down_revision = '977eda6841ef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uniq_db_user_01', 'db_user', ['first_name', 'surname', 'email', 'telephone'])
    op.create_unique_constraint('uniq_db_user_02', 'db_user', ['user_name'])


def downgrade():
    op.drop_constraint('uniq_db_user_01', 'db_user')
    op.drop_constraint('uniq_db_user_02', 'db_user')
