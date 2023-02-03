r"""
Add supported size conventions to the database.
"""

from m4db_database.orm.latest import SizeConvention


def populate_size_conventions(session):
    r"""
    Create size conventions.
    Args:
        session: the session to the database to which we add size conventions.

    Returns: None

    """
    session.add(SizeConvention(symbol="ESVD", description="Equivalent spherical volume diameter"))
    session.add(SizeConvention(symbol="ECVL", description="Equivalent cubic volume length"))
    session.commit()
