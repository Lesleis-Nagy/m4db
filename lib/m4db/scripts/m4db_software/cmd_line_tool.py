r"""
Perform m4db software related command actions.
"""
from enum import Enum

import typer
from typer import Option
from typer import Argument

import pandas as pd

from tabulate import tabulate

from m4db.orm.schema import Software

from m4db.sessions import get_session

from m4db.db.software.create import create_software

app = typer.Typer()

NAME = "Name"
VERSION = "Version"
DESCRIPTION = "Description"
URL = "URL"
CITATION = "Citation"
EXECUTABLE = "Executable"


class SoftwareFieldNames(str, Enum):
    name = "name"
    version = "version"
    executable = "executable"
    description = "description"
    url = "url"
    citation = "citation"


@app.command()
def list(csv_file: str = Option(None, help="if specified, save output to csv file instead of stdout.")):
    r"""
    List the software in the system.
    """
    session = get_session(nullpool=True)
    try:
        software_list = session.query(Software).all()

        # If there are no software items ...
        if len(software_list) == 0:
            # ... tell the user
            print("There are currently no items of software.")
        else:
            df_dict = {NAME: [],
                       VERSION: [],
                       DESCRIPTION: [],
                       URL: [],
                       CITATION: [],
                       EXECUTABLE: []}
            for software in software_list:
                df_dict[NAME].append(software.name)
                df_dict[VERSION].append(software.version)
                df_dict[DESCRIPTION].append(software.description)
                df_dict[URL].append(software.url)
                df_dict[CITATION].append(software.citation)
                df_dict[EXECUTABLE].append(software.executable)
            df = pd.DataFrame(df_dict)
            if csv_file:
                df.to_csv(csv_file, index=False)
            else:
                print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    finally:
        session.close()


@app.command()
def add(name: str = Argument(..., help="the new software name."),
        version: str = Argument(..., help="the new software version."),
        executable: str = Option(None, help="the full path / location for the software."),
        description: str = Option(None, help="a description for the new software."),
        url: str = Option(None, help="the URL at which the software can be found."),
        citation: str = Option(None, help="a citation for the software.")):
    r"""
    Adds a new m4db software item.
    """
    session = get_session(nullpool=True)

    try:
        software = create_software(
            session,
            name,
            version,
            executable,
            description,
            url,
            citation)
        session.add(software)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


@app.command()
def update(name: str = Argument(..., help="the name of the software to update."),
           version: str = Argument(..., help="the version of the software to update."),
           field: str = Argument(..., help="the field to update."),
           value: str = Argument(..., help="the new value of the required field.")):
    r"""
    Update or change some of a software's data items.
    """
    session = get_session(nullpool=True)

    try:
        software = session.query(Software) \
            .filter(Software.name == name, Software.version == version) \
            .one_or_none()

        if software is None:
            print(f"Software '{name}' at version '{version}' could not be found.")
        else:
            if field == SoftwareFieldNames.name.value:
                software.name = value
                session.commit()
            elif field == SoftwareFieldNames.version.value:
                software.version = value
                session.commit()
            elif field == SoftwareFieldNames.executable.value:
                software.executable = value
                session.commit()
            elif field == SoftwareFieldNames.description.value:
                software.description = value
                session.commit()
            elif field == SoftwareFieldNames.url.value:
                software.url = value
                session.commit()
            elif field == SoftwareFieldNames.citation.value:
                software.citation = value
                session.commit()
            else:
                print(f"Unknown field '{field}'")

    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


def entry_point():
    app()


if __name__ == "__main__":
    app()
