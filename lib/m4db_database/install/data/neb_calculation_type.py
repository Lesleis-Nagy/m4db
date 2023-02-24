r"""
Add supported NEB calculation types to the database.
"""

from m4db_database.orm.schema import NEBCalculationType


def populate_neb_calculation_types(session):
    r"""
    Creates calculation types and stores them in the database.
    Args:
        session: the session to the database.
    Returns:
        None
    """
    session.add(NEBCalculationType(name="fs_heuristic", description="Fabian & Shcherbakov 2019"))
    session.add(NEBCalculationType(name="neb", description="Henkelman et al. 2000"))
    session.commit()