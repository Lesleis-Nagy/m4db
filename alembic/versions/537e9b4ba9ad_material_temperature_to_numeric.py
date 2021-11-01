"""material temperature to numeric

Revision ID: 537e9b4ba9ad
Revises: a6ced65b75c7
Create Date: 2021-10-27 20:01:46.963111

"""
from alembic import op
from sqlalchemy import Numeric, String


# revision identifiers, used by Alembic.
revision = '537e9b4ba9ad'
down_revision = 'a6ced65b75c7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'material', 'temperature', type_=Numeric(8, 3), postgresql_using='temperature::numeric(8, 3)'
    )


def downgrade():
    op.alter_column(
        'material', 'temperature', type_=String, postgresql_using="temperature::varchar"
    )
