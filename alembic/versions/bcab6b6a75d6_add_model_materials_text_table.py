"""add model_materials_text table

Revision ID: bcab6b6a75d6
Revises: bb192523e255
Create Date: 2021-10-28 11:18:59.112198

"""
from alembic import op
from sqlalchemy import orm
from sqlalchemy import Column, Integer

from m4db_database.orm.v2_schema import ModelMaterialsText

# revision identifiers, used by Alembic.
revision = 'bcab6b6a75d6'
down_revision = 'bb192523e255'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Create the new table.
    ModelMaterialsText.__table__.create(bind)

    # Set up foreign key constraint
    op.add_column('model', Column('model_materials_text_id', Integer, nullable=False))
    op.create_foreign_key('model_model_materials_text_id_fkey',
                          'model',
                          'model_materials_text',
                          ['model_materials_text_id'],
                          ['id'])


def downgrade():
    # Drop the foreign key
    op.drop_constraint('model_model_materials_text_id_fkey', 'model', type_='foreignkey')
    op.drop_column('model', 'model_materials_text_id')

    # Drop the new table
    op.drop_table('model_materials_text')
