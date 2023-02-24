r"""
A collection of routines to create ModelMaterialsText objects.
"""

from m4db_database.orm.schema import ModelMaterialsText


def create_model_materials_text(json_model_dict, sep=","):
    r"""
    Retrieve a collection of model material associations from the database.
    :param json_model_dict: python dictionary (from JSON) holding information about our model. this
                            function focuses on the JSON part
                            {
                                ...
                                "materials": [
                                    {
                                        "name": <string>,
                                        "temperature": <decimal>,
                                        "submesh_id": <integer>
                                    }
                                ]
                                ...
                            }
    :param sep: separator character (default ',')
    :return: a ModelMaterialsText object.
    """

    # The list of material submesh indexes.
    submesh_index_list = []

    # The list of material names.
    material_list = []

    # The list of indices and materials names, i.e. ['1:magnetite', '2:iron',...]
    index_material_list = []

    # The list of index, material name and temperature, i.e. ['1:magnetite:40.000', '2:iron:40.000', ]
    index_material_temperature_list = []

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

            str_material_temperature = "{:20.3f}".format(material_temperature).strip()
            submesh_index_list.append(
                material_submesh_id)
            material_list.append(
                (material_submesh_id, material_name))
            index_material_list.append(
                (material_submesh_id, "{}:{}".format(material_submesh_id, material_name)))
            index_material_temperature_list.append(
                (material_submesh_id, "{}:{}:{}".format(material_submesh_id, material_name, str_material_temperature)))

    # Create a deduplicated version of submesh_index_list
    dedupe_submesh_index_list = list(dict.fromkeys(submesh_index_list))

    # If the length of dedupe_submesh_index_list and submesh_index_list are not the same ...
    if len(submesh_index_list) != len(dedupe_submesh_index_list):
        # ... there must be a repeated submesh, this is an error - close the session & raise error
        raise ValueError("New model JSON, a submesh index is repeated between materials.")

    # Sort material_list by material_submesh_id
    material_list.sort()

    # Sort index_material_list by material_submesh_id
    index_material_list.sort()

    # Sort index_material_temperature_list by material_submesh_id
    index_material_temperature_list.sort()

    # Create the ModelMaterialsText object
    mmt = ModelMaterialsText(
        materials=sep.join([p[1] for p in material_list]),
        submeshidxs_materials=sep.join(p[1] for p in index_material_list),
        submeshidxs_materials_temperatures = sep.join(p[1] for p in index_material_temperature_list)
    )

    return mmt
