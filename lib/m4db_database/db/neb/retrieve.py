r"""
A selection of routines to retrieve NEB paths from the database.
"""

from sqlalchemy import tuple_

from m4db_database.orm.schema import DBUser
from m4db_database.orm.schema import Geometry
from m4db_database.orm.schema import Material
from m4db_database.orm.schema import Metadata
from m4db_database.orm.schema import Model
from m4db_database.orm.schema import ModelMaterialAssociation
from m4db_database.orm.schema import RunningStatus
from m4db_database.orm.schema import SizeConvention
from m4db_database.orm.schema import Software
from m4db_database.orm.schema import Unit
from m4db_database.orm.schema import NEB


def get_nebs(session, **kwargs):
    r"""
    Retrieve a collection of NEBs according to the arguments passed.
    :param session: the database session.
    :param kwargs: argument parameters designed to filter specific types of NEB.
    :return: None
    """

    # Note, we join NEB with 'start_model' and use subsequent query parameters such as
    # geometry, material etc. with respect to that since the start and end models of an
    # NEB path should be the same in this regard.
    neb_query = session.query(NEB). \
        join(Model, Model.id == NEB.start_model_id). \
        join(RunningStatus, NEB.running_status_id == RunningStatus.id). \
        join(Geometry, Geometry.id == Model.geometry_id). \
        join(Unit, Unit.id == Geometry.size_unit_id). \
        join(SizeConvention, SizeConvention.id == Geometry.size_convention_id). \
        join(Metadata, Metadata.id == Model.mdata_id). \
        join(DBUser, DBUser.id == Metadata.db_user_id). \
        join(Software, Software.id == Metadata.software_id)

    print(f"running_status in the query: {kwargs['running_status']}")

    # Deal with the running status
    if "running_status" in kwargs.keys():
        if kwargs["running_status"] not in ["any", "all"]:
            neb_query = neb_query.filter(RunningStatus.name == kwargs["running_status"])

    # Deal with the geometry
    if "geometry" in kwargs.keys():
        neb_query = neb_query.filter(Geometry.name == kwargs["geometry"])
    if "size" in kwargs.keys():
        neb_query = neb_query.filter(Geometry.size == kwargs["size"])
    if "size_unit" in kwargs.keys():
        neb_query = neb_query.filter(Unit.symbol == kwargs["size_unit"])
    if "size_convention" in kwargs.keys():
        neb_query = neb_query.filter(SizeConvention.symbol == kwargs["size_convention"])

    # Deal with the metadata
    if "db_user" in kwargs.keys():
        neb_query = neb_query.filter(DBUser.user_name == kwargs["db_user"])
    #if "software" in kwargs.keys():
    #    neb_query = neb_query.filter(Software.name == kwargs["software"])
    #if "software_version" in kwargs.keys():
    #    neb_query = neb_query.filter(Software.version == kwargs["software_version"])

    # Deal with the materials.
    materials = None
    temperatures = None

    if "material" in kwargs.keys():
        materials = [kwargs["material"]]
    elif "materials" in kwargs.keys():
        materials = kwargs["materials"]
        if not isinstance(materials, list):
            raise ValueError("parameter 'materials' must be a list")

    # If we're given a singular temperature ...
    if "temperature" in kwargs.keys():
        # ... then, if we already have materials ...
        if materials is not None:
            # ... for each of those materials, use the temperature
            temperatures = [kwargs["temperature"]]*len(materials)
        else:
            # ... otherwise, there are no materials, so just use the temperature
            temperatures = [kwargs["temperature"]]
    # ... on the other hand, if we have plural temperatures
    elif "temperatures" in kwargs.keys():
        # ... assign the temperatures
        temperatures = kwargs["temperatures"]
        # ... and check that it's a list
        if not isinstance(temperatures, list):
            raise ValueError("parameter 'temperatures' must be a list")

    # If there are materials and temperatures
    if materials is not None and temperatures is not None:
        # ... each material must have a temperature to match.
        if len(materials) != len(temperatures):
            raise ValueError("Length of 'temperatures' and 'materials' should be the same")

    # Build the query

    if materials is not None and temperatures is None:
        # Case I there are material names, but no temperatures.
        for material in materials:
            subquery = session.query(Material.name). \
                join(ModelMaterialAssociation, ModelMaterialAssociation.material_id == Material.id). \
                filter(ModelMaterialAssociation.model_id == Model.id)
            neb_query = neb_query.filter(tuple_(material).in_(subquery))
    elif materials is None and temperatures is not None:
        # Case II there are no material names, but there are temperatures
        for temperature in temperatures:
            subquery = session.query(Material.temperature). \
                join(ModelMaterialAssociation, ModelMaterialAssociation.material_id == Material.id). \
                filter(ModelMaterialAssociation.model_id == Model.id)
            neb_query = neb_query.filter(tuple_(temperature).in_(subquery))
    elif materials is not None and temperatures is not None:
        # Case III there are both materials and temperatures
        for material, temperature in zip(materials, temperatures):
            subquery = session.query(Material.name, Material.temperature). \
                join(ModelMaterialAssociation, Material.id == ModelMaterialAssociation.material_id). \
                filter(ModelMaterialAssociation.model_id == Model.id)
            neb_query = neb_query.filter(tuple_(material, temperature).in_(subquery))

    # Retrieve the models.
    return neb_query.all()
