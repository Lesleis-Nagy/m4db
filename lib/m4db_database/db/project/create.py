r"""
A collection of routines for creating m4db projects.
"""

from m4db_database.orm.schema import Project


def create_project(session, project_name, project_description):
    r"""
    Create a new Project.
    :param session: a database session.
    :param project_name: the new project's name
    :param project_description: the new project's description
    :return:
    """
    project = session.query(Project).filter(Project.name == project_name).one_or_none()
    if project is not None:
        raise ValueError("Project with name '{}' already exists.".format(project_name))

    # Create a new Project
    project = Project(
        name=project_name,
        description=project_description
    )

    # Return the new project
    return project
