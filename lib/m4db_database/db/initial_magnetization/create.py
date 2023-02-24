r"""
A collection of routines to create model initial start fields.
"""

from m4db_database.orm.schema import Model
from m4db_database.orm.schema import RandomField
from m4db_database.orm.schema import UniformField
from m4db_database.orm.schema import ModelField
from m4db_database.orm.schema import Unit


def create_initial_magnetization(session, json_model_dict):
    r"""
    Create a field to be used as a start field for a micromagnetic model.
    :param session: a database session.
    :param json_model_dict: python dictionary (from JSON) holding information about our model,
                            this function focuses on the initial magnetization part

                            {
                                ...
                                "start_magnetization": {
                                    "type": "random",
                                    ["seed": <int>]
                                }
                                ...
                            }

                            or

                            {
                                ...
                                "start_magnetization": {
                                    "type": "uniform",
                                    "x_direction": <float>,
                                    "y_direction": <float>,
                                    "z_direction": <float>
                                }
                                ...
                            }

                            or

                            {
                                ...
                                "start_magnetization": {
                                    "type": "existing_model",
                                    "unique_id": <uuid>
                                }
                                ...
                            }
    :return: a new Field object.
    """
    start_magnetization = None

    # If the 'start_magnetization' is missing ...
    if "start_magnetization" not in json_model_dict.keys():
        # ... close session & raise error
        raise ValueError("New model JSON, 'start_magnetization' field is missing.")
    else:
        # ... retrieve the start_magnetization
        json_start_magnetization = json_model_dict["start_magnetization"]
        # If the json_start_magnetization is missing 'type' ...
        if "type" not in json_start_magnetization.keys():
            # ... close session & raise error
            raise ValueError("New model JSON, 'start_magnetization'.'type' is missing.")
        else:
            # ... process start_magnetization based on type
            start_magnetization_type = json_start_magnetization["type"]
            # If the start_magnetization_type is "random" ...
            if start_magnetization_type == "random":
                # ... process the random field.

                # If a seed is supplied then ...
                if "seed" in json_start_magnetization.keys():
                    # ... use the seed
                    seed = json_start_magnetization["seed"]
                else:
                    # ... otherwise set it to None
                    seed = None
                start_magnetization = RandomField(seed=seed)
            elif start_magnetization_type == "uniform":
                # ... otherwise, if the start_magnetization_type is "uniform" process the uniform field.
                unitless_unit = session.query(Unit).filter(Unit.symbol == "1").one()

                # If the json_start_magnetization has no x_direction field ...
                if "x_direction" not in json_start_magnetization.keys():
                    # ... close session & raise error
                    raise ValueError("New model JSON, start magnetization uniform field has no x direction.")
                else:
                    # ... othewise set start_magnetization_x_direction
                    start_magnetization_x_direction = json_start_magnetization["x_direction"]

                # If the json_start_magnetization has no y_direction field ...
                if "y_direction" not in json_start_magnetization.keys():
                    # ... close session & raise error
                    raise ValueError("New model JSON, start magnetization uniform field has no y direction.")
                else:
                    # ... set start_magnetization_y_direction
                    start_magnetization_y_direction = json_start_magnetization["y_direction"]

                # If the json_start_magnetization has no z_direction field ...
                if "z_direction" not in json_start_magnetization.keys():
                    # ... close session & raise error
                    raise ValueError("New model JSON, start magnetization uniform field has no z direction")
                else:
                    # ... set
                    start_magnetization_z_direction = json_start_magnetization["z_direction"]

                # Create a new uniform field start direction, note: magnitude is 1 here.
                start_magnetization = UniformField(
                    dx=start_magnetization_x_direction,
                    dy=start_magnetization_y_direction,
                    dz=start_magnetization_z_direction,
                    magnitude=1,
                    unit=unitless_unit
                )
            elif start_magnetization_type == "existing_model":
                # .. process existing model field.

                # If the json_start_magnetization has no unique_id field ...
                if "unique_id" not in json_start_magnetization.keys():
                    # ... close session & raise error
                    raise ValueError("New model JSON, start magnetization existing model, but unique_id is missing.")
                else:
                    start_magnetization_unique_id = json_start_magnetization["unique_id"]

                start_magnetization_model = session.query(Model).filter(Model.unique_id == start_magnetization_unique_id).one_or_none()
                if start_magnetization_model is None:
                    raise ValueError("New model JSON, start magnetization unique id '{}' not found.".format(
                        start_magnetization_unique_id
                    ))
                else:
                    start_magnetization = ModelField(model=start_magnetization_model)
            else:
                # .. close session & raise error
                raise ValueError("New model JSON, start magnetization unknown type: '{}'".format(
                    start_magnetization_type
                ))

    # If the start_magnetization couldn't be created ...
    if start_magnetization is None:
        # ... close session & raise error
        raise ValueError("Could not create model initial field.")

    return start_magnetization
