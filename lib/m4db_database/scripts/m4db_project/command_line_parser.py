
r"""
Create a command line parser to handle project server side scripts utility commands.
"""

from argparse import ArgumentParser


def default_project_subparser(subparsers):
    r"""
    Add a subparser to deal with setting default projectss.
        $> m4db_project set default <project name>
    :param subparsers: the subparsers objects.
    :return: a subparser.
    """
    subparser = subparsers.add_parser("default")

    subparser.add_argument("project", help="The m4db project name to use as a default.")
    subparser.add_argument("--force", action="store_true", help="Force change to config")

    return subparser


def set_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'set' command
        $> m4db_project set <set-commands>
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "set",
        help="Set m4db project data."
    )

    output = subparser.add_subparsers(dest="set_command")

    return output


def add_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'add' command
        $> m4db_project add <add-commands>
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "add",
        help="add a new m4db user."
    )

    subparser.add_argument("project_name", help="the new project's name")
    subparser.add_argument("description", help="the new projects's description")

    return subparser


def list_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'list' command
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    list_parser = subparsers.add_parser(
        "list",
        help="list m4db project data."
    )

    return list_parser


def command_line_parser():
    r"""
    Create a command line parser to handle project actions.
    :return: a command line parser
    """
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    set_subparser_obj = set_subparser(subparsers)
    list_subparser_obj = list_subparser(subparsers)
    add_subparser_obj = add_subparser(subparsers)

    default_project_subparser(set_subparser_obj)

    return parser
