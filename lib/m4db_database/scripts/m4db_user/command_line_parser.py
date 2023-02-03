from argparse import ArgumentParser

from m4db_database.utilities.access_levels import allowed_access_levels

from m4db_database import global_vars


def set_default_user_subparser(subparsers):
    r"""
    Add a subparser to deal with setting default users.
        $> m4db_user set default <db_user name>
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser("default")

    subparser.add_argument("db_user", help="the m4db user name to use as a default.")
    subparser.add_argument("--force", action="store_true", help="force change to config")

    return subparser


def set_password_subparser(subparsers):
    r"""
    Add a subparser to deal with setting a user's password.
        $> m4db_user set password <db_user name>
    :param subparsers: the subparsers object.
    :return: a subparser
    """
    subparser = subparsers.add_parser("password")

    subparser.add_argument("db_user", help="the m4db user name for which to set a new password.")

    return subparser


def set_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'set' command
        $> m4db_user set <set-commands>
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "set",
        help="Set m4db user data."
    )

    output = subparser.add_subparsers(dest="set_command")

    return output


def add_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'add' command
        $> m4db_user add <add-commands>
    :param subparsers: the subparsers object.
    :return: a subparser
    """
    subparser = subparsers.add_parser(
        "add",
        help="add a new m4db user."
    )

    subparser.add_argument("user_name", help="the new user's user name")
    subparser.add_argument("access_level", choices=allowed_access_levels(), help="the new user's access level")
    subparser.add_argument("first_name", help="the new user's first name")
    subparser.add_argument("surname", help="the new user's surname")
    subparser.add_argument("email", help="the user's email")

    subparser.add_argument(
        "--ticket-length",
        help="the length (s) of a new user's tickets (default={})".format(global_vars.default_db_user_ticket_length),
        default=global_vars.default_db_user_ticket_length)
    subparser.add_argument("--initials", help="the new user's initials")
    subparser.add_argument("--telephone", help="the new user's telephone number")

    return subparser


def list_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'list' command
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "list",
        help="List m4db user data."
    )

    return subparser


def command_line_parser():
    r"""
    Create a command line parser to handle user actions.
    :return: a command line parser
    """
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    set_subparser_obj = set_subparser(subparsers)
    list_subparser_obj = list_subparser(subparsers)
    add_subparser_obj = add_subparser(subparsers)

    set_default_user_subparser(set_subparser_obj)
    set_password_subparser(set_subparser_obj)

    return parser
