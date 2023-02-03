r"""
Add supported units to the databse.
"""
from m4db_database.orm.latest import Unit


def populate_units(session):
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