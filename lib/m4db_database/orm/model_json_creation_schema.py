r"""
Schema associated with the creation of new database objects.
"""

from enum import Enum

import schematics
import schematics.exceptions

from m4db_database import GLOBAL


######################################################################################################################
# Geometry schemas                                                                                                   #
######################################################################################################################
from m4db_database.orm.schema import AnisotropyFormEnum, SizeConventionEnum


class GeometrySchemaTypesEnum(Enum):
    ellipsoid = "ellipsoid"
    truncated_octahedron = "truncated-octahedron"


class EllipsoidSchema(schematics.models.Model):
    type = schematics.types.StringType(choices=[GeometrySchemaTypesEnum.ellipsoid.value], required=True)
    size = schematics.types.DecimalType(required=True)
    element_size = schematics.types.DecimalType(required=True, deserialize_from="element-size")
    size_convention = schematics.types.StringType(choices=[SizeConventionEnum.esvd.value,
                                                           SizeConventionEnum.ecvl.value], required=True,
                                                  deserialize_from="size-convention")
    oblateness = schematics.types.DecimalType(required=True)
    prolateness = schematics.types.DecimalType(required=True)


class TruncatedOctahedronSchema(schematics.models.Model):
    type = schematics.types.StringType(choices=[GeometrySchemaTypesEnum.truncated_octahedron.value], required=True)
    size = schematics.types.DecimalType(required=True)
    element_size = schematics.types.DecimalType(required=True, deserialize_from="element-size")
    size_convention = schematics.types.StringType(choices=[SizeConventionEnum.esvd.value,
                                                           SizeConventionEnum.ecvl.value], required=True,
                                                  deserialize_from="size-convention")
    aspect_ratio = schematics.types.DecimalType(required=True, deserialize_from="aspect-ratio")
    truncation_factor = schematics.types.DecimalType(required=True, deserialize_from="truncation-factor")


def geometry_claim_func(geometry, data):
    r"""
    Claim function will return a geometry schema classed based on the 'type' field.
    :param geometry: the geometry object.
    :param data: selection data.

    Returns: the geometry schema class corresponding to 'type' field.
    """
    if data["type"] == "ellipsoid":
        return EllipsoidSchema
    elif data["type"] == "truncated-octahedron":
        return TruncatedOctahedronSchema
    else:
        raise schematics.exceptions.ValidationError(f"Unknown geometry type: '{data['type']}'.")


######################################################################################################################
# Material schema                                                                                                    #
######################################################################################################################


class MaterialSchema(schematics.models.Model):
    r"""
    Schema object for validating Material data.
    """

    name = schematics.types.StringType(required=True)
    temperature = schematics.types.DecimalType(required=True)
    k1 = schematics.types.FloatType()
    k2 = schematics.types.FloatType()
    k3 = schematics.types.FloatType()
    k4 = schematics.types.FloatType()
    k5 = schematics.types.FloatType()
    k6 = schematics.types.FloatType()
    k7 = schematics.types.FloatType()
    k8 = schematics.types.FloatType()
    k9 = schematics.types.FloatType()
    k10 = schematics.types.FloatType()
    aex = schematics.types.FloatType()
    ms = schematics.types.FloatType()
    dir_x = schematics.types.FloatType(serialized_name="dir-x")
    dir_y = schematics.types.FloatType(serialized_name="dir-y")
    dir_z = schematics.types.FloatType(serialized_name="dir-z")
    submesh_id = schematics.types.IntType(default=1, serialized_name="submesh-id")

    anisotropy_form = schematics.types.StringType(choices=[AnisotropyFormEnum.cubic.value,
                                                           AnisotropyFormEnum.uniaxial.value],
                                                  serialized_name="anisotropy-form",
                                                  required=True)


def material_schema_list_is_valid(values):
    r"""
    Function to validate a list of materials.

    :param values: the list of materials.

    Returns: the input value and raises ValidationError on error.
    """

    # Validate each individual MaterialSchema
    for value in values:
        value.validate()

    # All temperatures must be the same
    temperatures = set(value.temperature for value in values)
    if len(temperatures) > 1:
        raise schematics.exceptions.ValidationError(
            u"When using multi-materials, all materials must have the same 'temperature' value.")

    # All submesh indices must be different
    submesh_ids = set(value.submesh_id for value in values)
    if len(values) != len(submesh_ids):
        raise schematics.exceptions.ValidationError(
            u"When using multi-materials, 'submesh-id' values must all be different")


######################################################################################################################
# Applied field schema                                                                                               #
######################################################################################################################


class AppliedFieldSchema(schematics.models.Model):
    r"""
    Schema object for validating applied fields data.
    """

    magnitude = schematics.types.FloatType(required=True)
    dir_x = schematics.types.FloatType(required=True, serialized_name="dir-x")
    dir_y = schematics.types.FloatType(required=True, serialized_name="dir-y")
    dir_z = schematics.types.FloatType(required=True, serialized_name="dir-z")


######################################################################################################################
# Initial magnetization schemas                                                                                      #
######################################################################################################################

class InitialMagnetizationSchemaTypesEnum(Enum):
    uniform = "uniform"
    model = "model"
    random = "random"


class UniformInitialMagnetizationSchema(schematics.models.Model):
    r"""
    Schema object for validating uniform initial field data.
    """

    type = schematics.types.StringType(required=True, choices=[InitialMagnetizationSchemaTypesEnum.uniform.value])
    magnitude = schematics.types.FloatType(required=True)
    dir_x = schematics.types.FloatType(required=True, serialized_name="dir-x")
    dir_y = schematics.types.FloatType(required=True, serialized_name="dir-y")
    dir_z = schematics.types.FloatType(required=True, serialized_name="dir-z")


class ModelInitialMagnetizationSchema(schematics.models.Model):
    r"""
    Schema object for validating existing model initial field schema.
    """

    type = schematics.types.StringType(required=True, choices=[InitialMagnetizationSchemaTypesEnum.model.value])
    unique_id = schematics.types.StringType(regex=GLOBAL.UID_REGEX, required=True, serialized_name="unique-id")


class RandomInitialMagnetizationSchema(schematics.models.Model):
    r"""
    Schema object for validating random initial field schema.
    """

    type = schematics.types.StringType(required=True, choices=[InitialMagnetizationSchemaTypesEnum.random.value])


def initial_magnetization_claim_func(field, data):
    r"""
    Claim function will return an initial magnetization schema class based on the 'type' field.
    :param field: the initial magnetization field object.
    :param data: selection data.

    Returns: the initial magnetization schema class corresponding to 'type' field.
    """
    if data["type"] == InitialMagnetizationSchemaTypesEnum.uniform.value:
        return UniformInitialMagnetizationSchema
    elif data["type"] == InitialMagnetizationSchemaTypesEnum.model.value:
        return ModelInitialMagnetizationSchema
    elif data["type"] == InitialMagnetizationSchemaTypesEnum.random.value:
        return RandomInitialMagnetizationSchema
    else:
        raise schematics.exceptions.ValidationError(f"Unknown initial magnetization type: '{data['type']}'.")


######################################################################################################################
# Model schema                                                                                                       #
######################################################################################################################


class ModelSchema(schematics.models.Model):
    r"""
    Schema object for validating new model schemas.
    """

    max_energy_evaluations = schematics.types.IntType(min_value=0, default="10000",
                                                      serialized_name="max-energy-evaluations")

    geometry = schematics.types.PolyModelType(
        [EllipsoidSchema, TruncatedOctahedronSchema],
        required=True,
        claim_function=geometry_claim_func
    )

    materials = schematics.types.ListType(schematics.types.ModelType(MaterialSchema),
                                          required=True,
                                          validators=[material_schema_list_is_valid])

    initial_magnetization = schematics.types.PolyModelType(
        [UniformInitialMagnetizationSchema, ModelInitialMagnetizationSchema, RandomInitialMagnetizationSchema],
        required=True,
        serialized_name="initial-magnetization",
        claim_function=initial_magnetization_claim_func
    )

    applied_field = schematics.types.ModelType(AppliedFieldSchema, serialized_name="applied-field")

    reps = schematics.types.IntType(min_value=1, default=1)


######################################################################################################################
# Model list schema                                                                                                  #
######################################################################################################################


class ModelListSchema(schematics.models.Model):
    r"""
    Schema object for validating a new set of models to add.
    """

    models = schematics.types.ListType(schematics.types.ModelType(ModelSchema))

