r"""
A collection of default data to add to the database.
"""


def create_materials(session, materials):
    r"""
    Create materials.

    Args:
        session: the session to the database to which materials are added.
        materials: a list of materials (currently 'magnetite' and 'iron' are supported).

    Returns: None

    """
    if materials is None:
        return

    anisotropy_form = session.query(AnisotropyForm).filter(AnisotropyForm.name == "cubic").one()

    temperature_start = 0.0
    temperature_step = 0.5

    for material in materials:
        if material == "iron":
            temperature_end = 770.5
        elif material == "magnetite":
            temperature_end = 579.5
        else:
            raise ValueError("Unknown material '{}'".format(material))

        temperature = temperature_start
        while temperature <= temperature_end:
            mparams = material_parameters(temperature, material)
            session.add(Material(
                name=material,
                temperature=decimal.Decimal(temperature),
                aex=mparams["Aex"],
                ms=mparams["Ms"],
                k1=mparams["K1"],
                kd=mparams["Kd"],
                lambda_ex=mparams["lambda_ex"],
                q_hardness=mparams["q_hardness"],
                anisotropy_form=anisotropy_form
            ))
            temperature += temperature_step
    session.commit()


