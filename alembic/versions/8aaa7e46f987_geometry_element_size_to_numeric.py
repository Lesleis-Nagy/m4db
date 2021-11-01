"""geometry element size to numeric

Revision ID: 8aaa7e46f987
Revises: bf87c71e3b90
Create Date: 2021-10-27 20:24:13.168454

"""
from alembic import op
from sqlalchemy import Numeric, String


# revision identifiers, used by Alembic.
revision = '8aaa7e46f987'
down_revision = 'bf87c71e3b90'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'geometry', 'element_size', type_=Numeric(10, 5), postgresql_using="size::numeric(10, 5)"
    )


def downgrade():
    op.alter_column(
        'geometry', 'element_size', type_=String, postgresql_using='size::varchar'
    )
