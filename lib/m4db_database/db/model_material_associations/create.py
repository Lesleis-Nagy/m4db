r"""
A collection of functions that retrieve material sets from the database.
"""

from m4db_database.orm.latest import Material
from m4db_database.orm.latest import ModelMaterialAssociation


def create_model_material_associations(session, json_model_dict):
    r"""
    Retrieve a collection of model material associations from the database.
    :param session: a database session.
    :param json_model_dict: python dictionary (from JSON) holding information about our model.
    :return: an array of ModelMaterialAssociation objects.
    """
    model_material_associations = []

    # If the 'materials' field is missing ...
    if "materials" not in json_model_dict.keys():
        # ... close session & raise error
        raise ValueError("New model JSON, 'materials' field is missing.")
    else:
        # ... retrieve materials
        json_materials = json_model_dict["materials"]
        for json_material in json_materials:
            # If the material JSON 'name' field is missing ...
            if "name" not in json_material.keys():
                # ... close session & raise error
                raise ValueError("New model JSON, material.'name' field is missing.")
            else:
                # ... set the material name
                material_name = json_material["name"]

            # If the material JSON 'temperature' field is missing ...
            if "temperature" not in json_material.keys():
                # ... close session & raise error
                raise ValueError("New model JSON, material.'temperature' field is missing.")
            else:
                # ... set the temperature
                material_temperature = json_material["temperature"]

            # If the material JSON 'submesh_id' is missing ...
            if "submesh_id" not in json_material.keys():
                # ... close session & raise error
                raise ValueError("New model JSON, material is missing.")
            else:
                material_submesh_id = json_material["submesh_id"]

            # Retrieve the material.
            material = session.query(Material). \
                filter(Material.name == material_name). \
                filter(Material.temperature == material_temperature). \
                one_or_none()

            # Create a new model-material association
            model_material_association = ModelMaterialAssociation(
                submesh_id=material_submesh_id,
                material=material
            )

            # Append model material association to the list of model material associations.
            model_material_associations.append(model_material_association)

    # If no materials could be found ...
    if len(model_material_associations) == 0:
        # ... close session & raise error
        raise ValueError("One or more material(s) could not be found.")

    return model_material_associations
