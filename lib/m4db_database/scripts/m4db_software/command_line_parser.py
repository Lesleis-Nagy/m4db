from argparse import ArgumentParser


def add_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'add' command
        $> m4db_software add <add-commands>
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "add",
        help="add a new m4db software item."
    )

    subparser.add_argument("name", help="the software name")
    subparser.add_argument("version", help="the software version")

    subparser.add_argument("--executable", help="the executable of the software")
    subparser.add_argument("--description", help="a description of the software")
    subparser.add_argument("--url", help="a url pointing to the software")
    subparser.add_argument("--citation", help="a citation to the software")

    return subparser


def list_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'list' command
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "list",
        help="list the m4db software data."
    )

    return subparser


def update_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'update' command
    :param subparsers: the subparsers object.
    :return: a subparser
    """
    subparser = subparsers.add_parser(
        "update",
        help="update the m4db software"
    )

    subparser.add_argument("name", help="the software name")
    subparser.add_argument("version", help="the software version")

    subparser.add_argument("--executable", help="the executable of the software")
    subparser.add_argument("--description", help="a description of the software")
    subparser.add_argument("--url", help="a url pointing to the software")
    subparser.add_argument("--citation", help="a citation to the software")

    return subparser


def command_line_parser():
    r"""
    Create a command line parser to handle project actions.
    :return: a command line parser
    """
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    list_subparser_obj = list_subparser(subparsers)
    add_subparser_obj = add_subparser(subparsers)
    update_subparser_obj = update_subparser(subparsers)

    return parser
