r"""
A collection of routines to retrieve size conventions from m4db.
"""

from m4db_database.orm.latest import SizeConvention


def allowed_size_conventions():
    r"""
    Retrieve a list of allowed size conventions.
    :return: a list of 3-tuples
    """
    return [
        ("ESVD", "Equivalent Spherical Volume Diameter"),
        ("ECVL", "Equivalent Cubic Volume Length")
    ]


def allowed_size_convention_symbols():
    r"""
    Retrieve a list of allowed size convention symbols.
    :return: a list of strings.
    """
    return list([p[0] for p in allowed_size_conventions()])


def valid_size_convention_symbol(symbol):
    r"""
    Check that the input symbol is a valid size convention.
    :param symbol: the size convention symbol.
    :return: True if symbol is a valid size convention symbol.
    """
    if symbol in allowed_size_convention_symbols():
        return True
    else:
        return False


def retrieve_size_convention(session, symbol):
    r"""
    Retrieve a size convention with the given symbol.
    :param session: a database session.
    :param symbol: the size convention symbol.
    :return: a SizeConvention object.
    """
    # Attempt to retrieve the SizeConvention
    size_convention = session.query(SizeConvention).filter(SizeConvention.symbol == symbol).one_or_none()
    # If the size convention cannot be found ...
    if size_convention is None:
        # ... raise error
        raise ValueError("Size convention with symbol '{}' cannot be found.".format(symbol))

    return size_convention
