r"""
A collection of functions that retrieve geometries from the database.
"""
from decimal import Decimal

from m4db_database.orm.schema import SizeConvention, Ellipsoid, TruncatedOctahedron
from m4db_database.orm.schema import SizeConventionEnum

from m4db_database.orm.model_json_creation_schema import GeometrySchemaTypesEnum


def get_geometry(session, **kwargs):
    if kwargs.get("schema_object") is not None:
        return get_geometry_by_schema_object(session, kwargs.get("schema_object"))
    elif kwargs.get("type") is not None:
        return get_geometry_by_type_and_kwargs(session, kwargs.get("type"), **kwargs)
    else:
        raise RuntimeError("Unknown input parameters for 'get_geometry'.")


def get_geometry_by_schema_object(session, schema_object):
    r"""
    Retrieve a geometry from the database using a schema object.

    :param session: the database session.
    :param schema_object: the schema object.

    :returns: a geometry

    """
    if schema_object.type == GeometrySchemaTypesEnum.ellipsoid.value:
        return get_ellipsoid(session,
                             Decimal(schema_object.size),
                             Decimal(schema_object.element_size),
                             SizeConventionEnum(schema_object.size_convention),
                             Decimal(schema_object.oblateness),
                             Decimal(schema_object.prolateness))
    elif schema_object.type == GeometrySchemaTypesEnum.truncated_octahedron.value:
        return get_truncated_octahedron(session,
                                        Decimal(schema_object.size),
                                        Decimal(schema_object.element_size),
                                        SizeConventionEnum(schema_object.size_convention),
                                        Decimal(schema_object.truncation_factor),
                                        Decimal(schema_object.aspect_ratio))
    else:
        raise RuntimeError("Unknown GeometryEnum type")


def get_geometry_by_type_and_kwargs(session, type: GeometrySchemaTypesEnum, **kwargs):
    r"""
    Retrieve a geometry from the database using keyword arguments.

    :param session: the database session.
    :param type: the database type.
    "param **kwargs: arguments for the geometry.

    :return: a geometry.

    """
    if type == GeometrySchemaTypesEnum.ellipsoid:
        return get_ellipsoid(
            session,
            Decimal(kwargs.get("size")),
            Decimal(kwargs.get("element_size")),
            SizeConventionEnum(kwargs.get("size_convention")),
            Decimal(kwargs.get("oblateness")),
            Decimal(kwargs.get("prolateness"))
        )
    elif type == GeometrySchemaTypesEnum.truncated_octahedron:
        return get_truncated_octahedron(
            session,
            Decimal(kwargs.get("size")),
            Decimal(kwargs.get("element_size")),
            SizeConventionEnum(kwargs.get("size_convention")),
            Decimal(kwargs.get("truncation_factor")),
            Decimal(kwargs.get("aspect_ratio"))
        )
    else:
        raise RuntimeError("Unknown GeometryEnum type")


def get_ellipsoid(session, size: Decimal, element_size: Decimal, size_convention: SizeConventionEnum,
                  oblateness: Decimal, prolateness: Decimal):
    r"""
    Retrieve an ellipsoid from the database.

    :param session:
    :param size:
    :param element_size:
    :param size_convention:
    :param oblateness:
    :param prolateness:

    :return: an existing ellipsoid object from the database.

    """
    return session.query(Ellipsoid).\
        join(SizeConvention, SizeConvention.id == Ellipsoid.size_convention_id). \
        filter(Ellipsoid.size == size). \
        filter(Ellipsoid.element_size == element_size). \
        filter(SizeConvention.symbol == size_convention.value). \
        filter(Ellipsoid.prolateness == prolateness). \
        filter(Ellipsoid.oblateness == oblateness). \
        one_or_none()


def get_truncated_octahedron(session, size: Decimal, element_size: Decimal, size_convention: SizeConventionEnum,
                             truncation_factor: Decimal, aspect_ratio: Decimal):
    r"""
    Retrieve a truncated octahedron from the database.

    :param session:
    :param size:
    :param element_size:
    :param size_convention:
    :param truncation_factor:
    :param aspect_ratio:

    :return: an existing truncated octahedron object from the database.

    """
    return session.query(TruncatedOctahedron). \
        join(SizeConvention, SizeConvention.id == TruncatedOctahedron.size_convention_id). \
        filter(TruncatedOctahedron.size == size). \
        filter(TruncatedOctahedron.element_size == element_size). \
        filter(SizeConvention.symbol == size_convention.value). \
        filter(TruncatedOctahedron.truncation_factor == truncation_factor). \
        filter(TruncatedOctahedron.aspect_ratio == aspect_ratio). \
        one_or_none()
