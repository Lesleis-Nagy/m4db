"""alter primary key of neb_model_split table

Revision ID: bb192523e255
Revises: 1ca450ab05de
Create Date: 2021-10-28 11:00:35.836474

"""
from alembic import op
from sqlalchemy import Column, Integer

# revision identifiers, used by Alembic.
revision = 'bb192523e255'
down_revision = '1ca450ab05de'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('neb_model_split', 'index')
    op.drop_constraint('neb_model_split_pkey', 'neb_model_split')
    op.add_column('neb_model_split', Column('id', Integer, primary_key=True))
    op.add_column('neb_model_split', Column('image_number', Integer))
    op.create_primary_key('neb_model_split_pkey', 'neb_model_split', ['id'])


def downgrade():
    op.drop_constraint('neb_model_split_pkey', 'neb_model_split')
    op.drop_column('neb_model_split', 'image_number')
    op.drop_column('neb_model_split', 'id')
    op.add_column('neb_model_split', Column('index', Integer, nullable=False))
    op.create_primary_key('neb_model_split_pkey', 'neb_model_split', ['neb_id', 'model_id'])
