r"""
Add supported anisotropy forms to the database.
"""

from m4db_database.orm.schema import AnisotropyForm


def populate_anisotropy_forms(session):
    r"""
    Create anisotropy forms.

    Args:
        session: the session to the database to which we add anisotorpy forms.

    Returns: None

    """
    session.add(AnisotropyForm(name="cubic", description="Cubic anisotorpy form"))
    session.add(AnisotropyForm(name="uniaxial", description="Uniaxial anisotropy form"))
    session.commit()
