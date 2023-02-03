r"""
Perform various m4db project related actions.
"""

import sys

from m4db_database.orm.latest import Project
from m4db_database.configuration import read_config_from_environ
from m4db_database.configuration import write_config_to_environ
from m4db_database.sessions import get_session

from m4db_database.db.project.create import create_project


def list_projects_action():
    r"""
    Display all projects in m4db.
    :return:
    """
    session = get_session(nullpool=True)

    try:
        projects = session.query(Project).all()

        # If there are no projects ...
        if len(projects) == 0:
            # ... tell the user
            print("There are currently no projects.")
        else:
            # ... otherwise print project information
            for project in projects:
                print("Print details for project: {}".format(project.name))
                print("   Description: {}".format(project.description))
                print("")
    finally:
        session.close()


def set_default_project_action(args):
    r"""
    Set the default project.
    :param args: command line arguments object.
    :return: None
    """
    project = args.project

    config = read_config_from_environ()

    # If force is true, just update and don't bother querying the database.
    if args.force:
        config["m4db_serverside"]["default_m4db_project"] = args.project
        write_config_to_environ(config)
        return

    # Get a session to the database.

    session = get_session(nullpool=True)

    # Retrieve the project.
    project = session.query(Project).filter(Project.name == args.project).one_or_none()

    # If the project could not be found ...
    if project is None:
        # ... inform the user.
        print("Project '{}' is not in the database.".format(args.project))
        # Terminate.
        session.close()
        sys.exit()
    else:
        config["m4db_serverside"]["default_m4db_project"] = args.project
        write_config_to_environ(config)
        session.close()
        return


def set_project_action(args):
    r"""
    Commands dealing with setting project.
    :param args: command line arguments.
    :return: None
    """

    if args.set_command == "default":
        set_default_project_action(args)


def add_project_action(args):
    r"""
    Adds a new m4db project.
    :param args: command line arguments.
    :return: None
    """
    session = get_session(nullpool=True)

    try:
        project = create_project(session, args.project_name, args.description)
        session.add(project)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()
