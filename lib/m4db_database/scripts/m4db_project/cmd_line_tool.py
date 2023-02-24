r"""
Perform various m4db project related actions.
"""

import typer

import pandas as pd

from tabulate import tabulate

from m4db_database.orm.schema import Project

from m4db_database.sessions import get_session

from m4db_database.db.project.create import create_project

app = typer.Typer()

NAME = "Name"
DESCRIPTION = "Description"

@app.command()
def list(csv_file: str = None):
    r"""
    Display all projects in m4db.

    :param csv_file save output to this csv file instead of writing to stdout.

    :return: None.
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
            df_dict = {NAME: [],
                       DESCRIPTION: []}
            for project in projects:
                df_dict[NAME].append(project.name)
                df_dict[DESCRIPTION].append(project.description)
            df = pd.DataFrame(df_dict)
            if csv_file:
                df.to_csv(csv_file, index=False)
            else:
                print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
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
