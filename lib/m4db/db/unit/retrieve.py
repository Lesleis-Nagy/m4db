r"""
A collection of routines to retrieve units from m4db.
"""

from m4db.orm.schema import Unit


def allowed_size_units():
    r"""
    Retrieve a list of allowed units.
    :return: a list of 3-tuples
    """
    return [
        ("m", "meter", 1),
        ("cm", "centimeter", 1e-02),
        ("mm", "millimeter", 1e-03),
        ("um", "micrometer", 1e-06),
        ("nm", "nanometer", 1e-09),
        ("pm", "picometer", 1e-12),
        ("fm", "femtometer", 1e-15),
        ("am", "attometer", 1e-18)
    ]


def allowed_field_units():
    r"""
    Retrieve a list of allowed field units.
    :return: a list of 3-tuples
    """
    return [
        ("T", "tesla", 1),
        ("mT", "millitesla", 1e-3),
        ("uT", "microtesla", 1e-06),
        ("nT", "nanotesla", 1e-09),
        ("pT", "picotesla", 1e-12),
        ("fT", "femtotesla", 1e-15),
        ("aT", "attotesla", 1e-18)
    ]


def allowed_size_unit_symbols():
    r"""
    Retrieve a list of allowed size unit symbols.
    :return: a list of strings.
    """
    return list([p[0] for p in allowed_size_units()])


def allowed_field_unit_symbols():
    r"""
    Retrieve a list of allowed field unit symbols.
    :return: a list of strings
    """
    return list(p[0] for p in allowed_field_units())


def valid_size_unit_symbol(symbol):
    r"""
    Check that the input symbol is a valid size unit.
    :param symbol: the size unit symbol.
    :return: True if symbol is a valid size unit symbol.
    """
    if symbol in allowed_size_unit_symbols():
        return True
    else:
        return False


def valid_field_unit_symbol(symbol):
    r"""
    Check that the input symbol is a valid field unit.
    :param symbol: the field unit symbol
    :return: True if symbol is a valid field unit symbol
    """
    if symbol in allowed_field_unit_symbols():
        return True
    else:
        return False


def retrieve_unit(session, symbol):
    r"""
    Retrieve a unit with the given symbol.
    :param session: a database session.
    :param symbol: the unit symbol.
    :return: a Unit object.
    """
    # Attempt to retrieve the Unit
    unit = session.query(Unit).filter(Unit.symbol == symbol).one_or_none()
    # If the unit cannot be found ...
    if unit is None:
        # ... raise error
        raise ValueError("Unit with symbol '{}' cannot be found.".format(symbol))

    return unit
