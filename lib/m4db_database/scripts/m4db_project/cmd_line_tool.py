r"""
Perform various m4db project related actions.
"""

import typer

from tabulate import tabulate

from m4db_database.orm.latest import Project

from m4db_database.sessions import get_session

from m4db_database.db.project.create import create_project

app = typer.Typer()


@app.command()
def list():
    r"""
    Display all projects in m4db.
    :return: None
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


@app.command()
def add(project_name: str, description: str):
    r"""
    Adds a new m4db project.
    :param project_name: name of the new project.
    :param description: description for the new project.
    :return: None
    """
    session = get_session(nullpool=True)

    try:
        project = create_project(
            session,
            project_name,
            description
        )
        session.add(project)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


def entry_point():
    app()


if __name__ == "__main__":
    app()
