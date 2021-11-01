"""geometry size to numeric

Revision ID: bf87c71e3b90
Revises: 537e9b4ba9ad
Create Date: 2021-10-27 20:17:57.789139

"""
from alembic import op
from sqlalchemy import Numeric, String


# revision identifiers, used by Alembic.
revision = 'bf87c71e3b90'
down_revision = '537e9b4ba9ad'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'geometry', 'size', type_=Numeric(10, 5), postgresql_using="size::numeric(10, 5)"
    )


def downgrade():
    op.alter_column(
        'geometry', 'size', type_=String, postgresql_using='size::varchar'
    )
