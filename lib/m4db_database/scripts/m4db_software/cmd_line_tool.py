r"""
Perform m4db software related command actions.
"""

from enum import Enum

import sys
import typer

from m4db_database import GLOBAL

from m4db_database.orm.latest import Software

from m4db_database.sessions import get_session

from m4db_database.db.software.create import create_software
from m4db_database.db.software.retrieve import retrieve_software

app = typer.Typer()


class SoftwareFieldNames(str, Enum):
    name = "name"
    version = "version"
    executable = "executable"
    description = "description"
    url = "url"
    citation = "citation"


@app.command()
def list():
    r"""
    Display all software in m4db
    :return: None
    """
    session = get_session(nullpool=True)

    try:
        software_list = session.query(Software).all()
        # If there are no software items ...
        if len(software_list) == 0:
            # ... tell the user
            print("There are currently no items of software.")
        else:
            # ... otherwise print software information
            for software in software_list:
                print("Details for software: {}".format(software.name))
                print("   Version:     {}".format(software.version))
                print("   Description: {}".format(software.description))
                print("   URL:         {}".format(software.url))
                print("   Citation:    {}".format(software.citation))
                print("   Executable:  {}".format(software.executable))
                print("")
    finally:
        session.close()


@app.command()
def add(name: str, version: str, executable: str = None, description: str = None, url: str = None,
        citation: str = None):
    r"""
    Adds a new m4db software item.
    :param name: the new software name.
    :param version: the new software version.
    :param executable: the full path / location for the software.
    :param description: a description for the new software.
    :param url: the URL at which the software can be found.
    :param citation: a citation for the software.
    :return: None
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
            citation
        )
        session.add(software)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


@app.command()
def update(software_and_version: str, field: SoftwareFieldNames, value: str):
    r"""
    Updates some of a software's data items
    :param software: the name of the software and version separated by an '@' symbol,
                     for example merrill@1.8.1.
    :param field: the field to update.
    :param value: the new value of the required field.
    :return: None
    """
    match_sw_ver = GLOBAL.REGEX_SOFTWARE_AND_VERSION.match(software_and_version)
    if match_sw_ver:

        name = match_sw_ver.group(1)
        version = match_sw_ver.group(2)

        session = get_session(nullpool=True)

        try:
            software = retrieve_software(session, name, version)

            if field == "name":
                software.name = value
            elif field == "version":
                software.version = value
            elif field == "executable":
                software.executable = value
            elif field == "description":
                software.description = value
            elif field == "url":
                software.url = value
            elif field == "citation":
                software.citation = value
            else:
                print(f"Unknown field '{field}'")
                sys.exit(1)
            session.commit()

        except ValueError as exception_obj:
            print(str(exception_obj))
        finally:
            session.close()
            sys.exit(1)

    else:

        print(f"Software and version '{software_and_version}' are not in the correct format.")


def entry_point():
    app()


if __name__ == "__main__":
    app()
