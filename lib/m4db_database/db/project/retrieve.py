r"""
A collection of routines to retrieve project info from the database.
"""

from m4db_database.orm.latest import Project


def retrieve_project(session, project_name):
    r"""
    Retrieve project info from the database.
    :param session: a database session.
    :param project_name: the name of the project to retrieve.
    :return: A Project object.
    """
    # Attempt to retrieve the project
    project = session.query(Project).\
        filter(Project.name == project_name).\
        one_or_none()
    # If the project cannot be found ...
    if project is None:
        # ... close session & raise error
        raise ValueError("New model project '{}' cannot be found.".format(project_name))

    return project
