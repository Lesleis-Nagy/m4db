from argparse import ArgumentParser


def model_general_subparser(subparsers):
    r"""
    Add a subparser to deal with the 'model-general' command.
    :param subparsers: the subparsers object.
    :return: a subparser.
    """
    subparser = subparsers.add_parser(
        "model-general",
        help="provide general assay statistics for models"
    )
    return subparser


def neb_general_subparser(subparsers):
    r"""
    Add a subparser to deal with 'neb-general' command.
    :param subparsers: the subparsers object.
    :return: a subparser
    """
    subparser = subparsers.add_parser(
        "neb-general",
        help="provide general assay statistics for NEBs"
    )
    return subparser


def command_line_parser():
    r"""
    Create a command line parser to handle user actions.
    :return: a command line parser.
    """
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    model_general_subparser_obj = model_general_subparser(subparsers)
    neb_general_subparser_obj = neb_general_subparser(subparsers)

    return parser
