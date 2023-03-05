r"""
A collection of routines to retrieve software info from the database.
"""

from m4db.orm.schema import Software


def retrieve_software(session, software_name, software_version: str, allow_none=False):
    r"""
    Retrieve software info from the database.
    :param session: a database session.
    :param software_name: the name of the software to retrieve.
    :param software_version: the version of the software to retrieve.
    :return: A Software object.
    """
    # Attempt to retrieve the software
    software = session.query(Software). \
        filter(Software.name == software_name). \
        filter(Software.version == str(software_version)). \
        one_or_none()

    # If the software cannot be found ...
    if software is None:
        # If we're allowing None as a return value ...
        if allow_none:
            # ... return None
            return None
        else:
            # ... otherwise raise error
            raise ValueError(
                "Software {} (version: {}) cannot be found.".format(software_name, software_version))

    return software
