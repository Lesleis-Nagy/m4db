r"""
Perform various actions.
"""

import sys

from getpass import getpass

from m4db_database.orm.latest import DBUser
from m4db_database.configuration import read_config_from_environ
from m4db_database.configuration import write_config_to_environ

from m4db_database.sessions import get_session

from m4db_database.db.db_user.create import create_db_user

from m4db_database.utilities.access_levels import string_to_access_level


def list_users_action():
    r"""
    Create a new model from input piped from stdin.
    :return:
    """
    session = get_session(nullpool=True)
    try:
        users = session.query(DBUser).all()

        # If there are no m4db users ...
        if len(users) == 0:
            # ... tell the user
            print("There are currently no database users.")
        else:
            # ... otherwise print user information
            for user in users:
                print("Print details for user: {}".format(user.user_name))
                print("   First name: {}".format(user.first_name))
                print("   Initials:   {}".format(user.initials))
                print("   Surname:    {}".format(user.surname))
                print("   Email:      {}".format(user.email))
                print("   Telephone:  {}".format(user.telephone))
                print("")
    finally:
        session.close()


def set_default_user_action(args):
    r"""
    Set the default user - this is the default server-side user so any actions on the database (such as adding new
    models) will use this user.
    :param args: command line arguments object.
    :return: None
    """

    config = read_config_from_environ()

    # If force is true, just update and don't bother querying the database.
    if args.force:
        config["m4db_serverside"]["default_m4db_user"] = args.db_user
        write_config_to_environ(config)
        return

    # Get a session to the database.
    session = get_session(nullpool=True)

    # Retrieve the user.
    db_user = session.query(DBUser).filter(DBUser.user_name == args.db_user).one_or_none()

    # If the user could not be found ...
    if db_user is None:
        # ... inform the user.
        print("User '{}' is not in the database.".format(args.db_user))
        # Terminate.
        session.close()
        sys.exit()
    else:
        # ... update (as long as global_vars.m4db_serverside_config_environment_variable exists)
        config["m4db_serverside"]["default_m4db_user"] = args.db_user
        write_config_to_environ(config)
        session.close()
        return


def set_user_action(args):
    r"""
    Commands dealing with setting users.
    :param args: command line arguments.
    :return: None
    """
    if args.set_command == "default":
        set_default_user_action(args)


def add_user_action(args):
    r"""
    Adds a new database user.
    :param args: command line arguments.
    :return: None
    """
    session = get_session(nullpool=True)

    access_level = string_to_access_level(args.access_level)

    try:
        db_user = create_db_user(
            args.user_name,
            args.first_name,
            args.surname,
            args.email,
            access_level,
            args.ticket_length,
            session,
            args.initials,
            args.telephone)
        session.add(db_user)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()
