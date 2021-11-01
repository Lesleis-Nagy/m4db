"""Initial database

Revision ID: a6ced65b75c7
Revises:
Create Date: 2021-10-27 17:55:04.887530

"""

from alembic import op
from sqlalchemy import orm

from m4db_database.orm.v1_schema import *

# revision identifiers, used by Alembic.
revision = 'a6ced65b75c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # Create tables based on ORM
    DBUser.__table__.create(bind)
    Software.__table__.create(bind)
    Unit.__table__.create(bind)
    PhysicalConstant.__table__.create(bind)
    SizeConvention.__table__.create(bind)
    AnisotropyForm.__table__.create(bind)
    Geometry.__table__.create(bind)
    Material.__table__.create(bind)
    Field.__table__.create(bind)
    FileField.__table__.create(bind)
    RandomField.__table__.create(bind)
    UniformField.__table__.create(bind)
    RunningStatus.__table__.create(bind)
    ModelRunData.__table__.create(bind)
    ModelReportData.__table__.create(bind)
    Project.__table__.create(bind)
    Metadata.__table__.create(bind)
    LegacyModelInfo.__table__.create(bind)
    Model.__table__.create(bind)
    ModelField.__table__.create(bind)
    ModelMaterialAssociation.__table__.create(bind)
    NEBCalculationType.__table__.create(bind)
    NEBRunData.__table__.create(bind)
    NEBReportData.__table__.create(bind)
    NEB.__table__.create(bind)
    NEBModelSplit.__table__.create(bind)
    MGSTStartEndPairCount.__table__.create(bind)


def downgrade():
    pass
