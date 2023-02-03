r"""
Perform various m4db software related command actions.
"""

from m4db_database.orm.latest import Software

from m4db_database.sessions import get_session

from m4db_database.db.software.create import create_software
from m4db_database.db.software.retrieve import retrieve_software


def list_software_actions():
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
                print("")
    finally:
        session.close()


def add_software_action(args):
    r"""
    Adds a new m4db software item.
    :param args: command line arguments.
    :return: None
    """
    session = get_session(nullpool=True)

    try:
        software = create_software(session, args.name, args.version, args.executable, args.description, args.url, args.citation)
        session.add(software)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


def update_software_action(args):
    r"""
    Updates some of a software's data items
    :param args: command line arguments
    :return: None
    """
    session = get_session(nullpool=True)

    try:
        software = retrieve_software(session, args.name, args.version)
        if args.executable:
            software.executable = args.executable
        if args.description:
            software.description = args.description
        if args.url:
            software.url = args.url
        if args.citation:
            software.citation = args.citation
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


