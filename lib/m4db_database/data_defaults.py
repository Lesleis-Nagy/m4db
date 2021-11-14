r"""
A collection of default data to add to the database.
"""

import decimal

from m4db_database.orm.latest import RunningStatus
from m4db_database.orm.latest import Unit
from m4db_database.orm.latest import SizeConvention
from m4db_database.orm.latest import Material
from m4db_database.orm.latest import AnisotropyForm

from m4db_database.materials import material_parameters


def create_units(session):
    r"""
    Creates units and stores them in the database.
    Args:
        session: the session to the database to which we add units.

    Returns: None

    """
    session.add(Unit(symbol="1", name="unitless", power=1))
    session.add(Unit(symbol="m", name="meter", power=1))
    session.add(Unit(symbol="cm", name="centimeter", power=0.01))
    session.add(Unit(symbol="mm", name="millimeter", power=0.001))
    session.add(Unit(symbol="um", name="micrometer", power=1e-06))
    session.add(Unit(symbol="nm", name="nanometer", power=1e-09))
    session.add(Unit(symbol="pm", name="picometer", power=1e-12))
    session.add(Unit(symbol="fm", name="femtometer", power=1e-15))
    session.add(Unit(symbol="am", name="attometer", power=1e-18))
    session.add(Unit(symbol="T", name="tesla", power=1))
    session.add(Unit(symbol="mT", name="millitesla", power=0.001))
    session.add(Unit(symbol="uT", name="microtesla", power=1e-06))
    session.add(Unit(symbol="nT", name="nanotesla", power=1e-09))
    session.add(Unit(symbol="pT", name="picotesla", power=1e-12))
    session.add(Unit(symbol="fT", name="femtotesla", power=1e-15))
    session.add(Unit(symbol="aT", name="attotesla", power=1e-18))
    session.commit()


def create_running_statuses(session):
    r"""
    Create running statues.
    Args:
        session: the session to the database to which we add running statues.

    Returns: None

    """
    session.add(RunningStatus(name="not-run", description="a model that has not been run yet"))
    session.add(RunningStatus(name="re-run", description="a model that is scheduled for a re-run"))
    session.add(RunningStatus(name="running", description="a model that is currently running scheduled to run"))
    session.add(RunningStatus(name="finished", description="a model that is finished running"))
    session.add(RunningStatus(name="crashed", description="a model that has crashed"))
    session.add(RunningStatus(name="scheduled", description="a job that has been scheduled for running"))
    session.commit()


def create_anisotropy_forms(session):
    r"""
    Create anisotropy forms.

    Args:
        session: the session to the database to which we add anisotorpy forms.

    Returns: None

    """
    session.add(AnisotropyForm(name="cubic", description="Cubic anisotorpy form"))
    session.add(AnisotropyForm(name="uniaxial", description="Uniaxial anisotropy form"))
    session.commit()


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


def create_size_conventions(session):
    r"""
    Create size conventions.
    Args:
        session: the session to the database to which we add size conventions.

    Returns: None

    """
    session.add(SizeConvention(symbol="ESVD", description="Equivalent spherical volume diameter"))
    session.add(SizeConvention(symbol="ECVL", description="Equivalent cubic volume length"))
    session.commit()
