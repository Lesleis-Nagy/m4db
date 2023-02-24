r"""
A selection of routines for creating software objects.
"""

from m4db_database.orm.schema import Software


def create_software(session, name, version, executable, description, url, citation):
    r"""
    Create a new software object
    :param session: a database session.
    :param name: the name of the software.
    :param version: the version
    :param executable: the executable
    :param description: a description of the software
    :param url: a url to find the software
    :param citation: a citation or DOI
    :return:
    """
    # Check that the software is not already in the database.
    software = session.query(Software).\
        filter(Software.name == name).\
        filter(Software.version == version).\
        one_or_none()

    if software is not None:
        raise ValueError("The software {} (version: {}) already exists".format(name, version))

    software = Software(
        name=name,
        version=version,
        executable=executable,
        description=description,
        url=url,
        citation=citation
    )

    return software
