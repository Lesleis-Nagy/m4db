r"""
A collection of functions that retrieve geometries from the database.
"""

from m4db_database.orm.latest import SizeConvention
from m4db_database.orm.latest import Unit
from m4db_database.orm.latest import Geometry


def retrieve_geometry(session, json_model_dict):
    r"""
    Retrieve a geometry from the session given a JSON model dictionary.
    :param session: a database session.
    :param json_model_dict: python dictionary (parsed from JSON) holding information about our model, this
                            function focuses on the JSON part
                            {
                                ...
                                "geometry": {
                                    "name": <string>,
                                    "size": <decimal>,
                                    "size_convention": <string>,
                                    "size_unit": <string>
                                }
                                ...
                            }

    :return: an existing Geometry object.
    """
    geometry = None

    # If the 'geometry' field is missing ...
    if "geometry" not in json_model_dict.keys():
        # ... close session & raise error
        raise ValueError("New model JSON, 'geometry' field is missing.")
    else:
        # ... attempt to retrieve the Geometry from m4db
        json_geometry = json_model_dict["geometry"]

        # If the geometry JSON 'name' field is missing ...
        if "name" not in json_geometry.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, 'geometry'.'name' field is missing.")
        else:
            # ... retrieve the name
            name = json_geometry["name"]

        # If the geometry JSON 'size' field is missing ...
        if "size" not in json_geometry.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, 'geometry'.'size' field is missing.")
        else:
            # ... retrieve the size
            size = json_geometry["size"]

        # If the geometry JSON 'size_convention' is missing ...
        if "size_convention" not in json_geometry.keys():
            # ... set default to 'ESVD'
            size_convention = 'ESVD'
        else:
            # ... set the size_convention
            size_convention = json_geometry["size_convention"]

        # If the geometry JSON 'size_unit' is missing ...
        if "size_unit" not in json_geometry.keys():
            # ... set default to 'um'
            size_unit = 'um'
        else:
            # ... set the size_unit
            size_unit = json_geometry["size_unit"]

        geometry = session.query(Geometry). \
            join(SizeConvention, Geometry.size_convention_id == SizeConvention.id). \
            join(Unit, Geometry.size_unit_id == Unit.id). \
            filter(Geometry.name == name). \
            filter(Geometry.size == size). \
            filter(SizeConvention.symbol == size_convention). \
            filter(Unit.symbol == size_unit). \
            one_or_none()

    # If the geometry could not be found ...
    if geometry is None:
        # ... close session & raise error
        raise ValueError("Model geometries could not be found.")
    else:
        return geometry
