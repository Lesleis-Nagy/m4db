r"""
A selection of routines to retrieve models from the database.
"""
from sqlalchemy import tuple_

from m4db_database.orm.schema import DBUser
from m4db_database.orm.schema import Geometry
from m4db_database.orm.schema import Material
from m4db_database.orm.schema import Metadata
from m4db_database.orm.schema import Model
from m4db_database.orm.schema import RunningStatus
from m4db_database.orm.schema import SizeConvention
from m4db_database.orm.schema import Software


def get_models(session, **kwargs):
    r"""
    Retrieve a collection of models according to the arguments passed.
    :param session: the database session.
    :param kwargs: argument parameters designed to filter specific types of model.
    :return: None
    """
    models_query = session.query(Model). \
        join(RunningStatus, Model.running_status_id == RunningStatus.id). \
        join(Geometry, Geometry.id == Model.geometry_id). \
        join(SizeConvention, SizeConvention.id == Geometry.size_convention_id). \
        join(Metadata, Metadata.id == Model.mdata_id). \
        join(DBUser, DBUser.id == Metadata.db_user_id). \
        join(Software, Software.id == Metadata.software_id)

    # Deal with the running status
    if "running_status" in kwargs.keys():
        if kwargs["running_status"] not in ["any", "all"]:
            models_query = models_query.filter(RunningStatus.name == kwargs["running_status"])

    # Deal with the geometry
    if "geometry" in kwargs.keys():
        models_query = models_query.filter(Geometry.name == kwargs["geometry"])
    if "size" in kwargs.keys():
        models_query = models_query.filter(Geometry.size == kwargs["size"])
    if "size_unit" in kwargs.keys():
        models_query = models_query.filter(Unit.symbol == kwargs["size_unit"])
    if "size_convention" in kwargs.keys():
        models_query = models_query.filter(SizeConvention.symbol == kwargs["size_convention"])

    # Deal with the metadata
    if "db_user" in kwargs.keys():
        models_query = models_query.filter(DBUser.user_name == kwargs["db_user"])
    if "software" in kwargs.keys():
        models_query = models_query.filter(Software.name == kwargs["software"])
    if "software_version" in kwargs.keys():
        models_query = models_query.filter(Software.version == kwargs["software_version"])

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
            models_query = models_query.filter(tuple_(material).in_(subquery))
    elif materials is None and temperatures is not None:
        # Case II there are no material names, but there are temperatures
        for temperature in temperatures:
            subquery = session.query(Material.temperature). \
                join(ModelMaterialAssociation, ModelMaterialAssociation.material_id == Material.id). \
                filter(ModelMaterialAssociation.model_id == Model.id)
            models_query = models_query.filter(tuple_(temperature).in_(subquery))
    elif materials is not None and temperatures is not None:
        # Case III there are both materials and temperatures
        for material, temperature in zip(materials, temperatures):
            subquery = session.query(Material.name, Material.temperature). \
                join(ModelMaterialAssociation, Material.id == ModelMaterialAssociation.material_id). \
                filter(ModelMaterialAssociation.model_id == Model.id)
            models_query = models_query.filter(tuple_(material, temperature).in_(subquery))

    # Retrieve the models.
    return models_query.all()


def get_model_quants(session, **kwargs):
    r"""
    Retrieve a collection of model quants according to the arguments passed.
    :param session: the database session.
    :param kwargs: argument parameters designed to filter specific types of model.
    :return: None
    """
    models = get_models(session, **kwargs)

    quants = []
    for model in models:
        quants.append({
            "mx_tot": model.mx_tot,
            "my_tot": model.my_tot,
            "mz_tot": model.mz_tot,
            "vx_tot": model.vx_tot,
            "vy_tot": model.vy_tot,
            "vz_tot": model.vz_tot,
            "h_tot": model.h_tot,
            "rh_tot": model.rh_tot,
            "adm_tot": model.adm_tot,
            "e_typical": model.e_typical,
            "e_anis": model.e_anis,
            "e_ext": model.e_ext,
            "e_demag": model.e_demag,
            "e_exch1": model.e_exch1,
            "e_exch2": model.e_exch2,
            "e_exch3": model.e_exch3,
            "e_exch4": model.e_exch4,
            "e_tot": model.e_tot,
            "volume": model.volume
        })

    return quants
