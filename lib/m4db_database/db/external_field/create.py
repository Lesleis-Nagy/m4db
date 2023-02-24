r"""
A collection of routines to create external field objects
"""

from m4db_database.orm.schema import Unit
from m4db_database.orm.schema import UniformField


def create_external_field(session, json_model_dict):
    r"""
    Create a field to be used as the external field for a micromagnetic model.
    :param session: a database session.
    :param json_model_dict: python dictionary (from JSON) holding information about our model, this function
                            focuses on the JSON part
                            {
                                ...
                                "external_field": {
                                    "x_direction": <float>,
                                    "y_direction": <float>,
                                    "z_direction": <float>,
                                    "strength": <float>,
                                    "unit": <float>
                                }
                                ...
                            }
                            Note: 1) external field unit defaults to uT,
                                  2) the external field entry is entirely optional.

    :return: a new UniformField object or None.
    """
    external_field = None

    # If the external field is present
    if "external_field" in json_model_dict.keys():
        # ... retrieve the external field json data
        json_external_field = json_model_dict["external_field"]

        # If the json_external_field has no x_direction field ...
        if "x_direction" not in json_external_field.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, external field has no x direction.")
        else:
            # ... othewise set external_field_x_direction
            external_field_x_direction = json_external_field["x_direction"]

        # If the json_external_field has no y_direction field ...
        if "y_direction" not in json_external_field.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, external field has no y direction.")
        else:
            # ... set external_field_y_direction
            external_field_y_direction = json_external_field["y_direction"]

        # If the json_external_field has no z_direction field ...
        if "z_direction" not in json_external_field.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, external field has no z direction")
        else:
            # ... set external_field_z_direction
            external_field_z_direction = json_external_field["z_direction"]

        # If the json_external field has no strength ...
        if "strength" not in json_external_field.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, external field has no magnitude")
        else:
            # ... set external_field_magnitude
            external_field_magnitude = json_external_field["strength"]

        # If the json_external_field has no unit ...
        if "unit" not in json_external_field.keys():
            # ... set unit to default value of micro Tesla
            field_unit = "uT"
        else:
            field_unit = json_external_field["unit"]

        # Retrieve the unit
        external_field_unit = session.query(Unit).filter(Unit.symbol == field_unit).one_or_none()

        # If external_field_unit could not be found
        if external_field_unit is None:
            # ... close session & raise error.
            raise ValueError("New model JSON, unknown field unit: '{}'".format(field_unit))

        # Build a new external field object
        external_field = UniformField(
            dx=external_field_x_direction,
            dy=external_field_y_direction,
            dz=external_field_z_direction,
            magnitude=external_field_magnitude,
            unit=external_field_unit
        )

    return external_field
