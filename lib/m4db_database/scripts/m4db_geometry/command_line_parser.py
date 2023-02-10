from argparse import ArgumentParser

from m4db_database.db.unit.retrieve import allowed_size_unit_symbols
from m4db_database.db.size_convention.retrieve import allowed_size_convention_symbols


def add_subparser(subparsers):
    r"""
    Adds a subparser to the input subparsers to deal with the 'add' command
        $> m4db_geometry add <add-commands>
    :param subparsers: the subparsers object that will take the new subparser
    :return: a subparser
    """
    add_subparser = subparsers.add_parser(
        "add",
        help="add a new m4db geometry."
    )

    add_subparser.add_argument("geometry_name",
                               help="the name of the new geometry")
    add_subparser.add_argument("geometry_size",
                               help="the size of the new geometry")
    add_subparser.add_argument("geometry_size_unit",
                               help="the size unit of the new geometry",
                               choices=allowed_size_unit_symbols())
    add_subparser.add_argument("geometry_size_convention",
                               help="the size convention of the new geometry",
                               choices=allowed_size_convention_symbols())
    add_subparser.add_argument("patran_file",
                               help="the name of the patran file containing new geometry information")
    add_subparser.add_argument("software_name",
                               help="the name of the software used to crate the new geometry patran file")
    add_subparser.add_argument("software_version",
                               help="the version of the software used to create the new geometry patran file")

    # Optional arguments
    add_subparser.add_argument("--geometry-description",
                               help="a description of the new geometry")
    add_subparser.add_argument("--software-url",
                               help="the URL at which to find the meshing software")
    add_subparser.add_argument("--software-description",
                               help="a description of the meshing software")
    add_subparser.add_argument("--software-citation",
                               help="a citation or DOI of the meshing software")
    add_subparser.add_argument("--patran-generation-script",
                               help="script used to generate the new geometry patran file")
    add_subparser.add_argument("--patran-generation-stdout",
                               help="standard output of the meshing")

    return add_subparser


def command_line_parser():
    r"""
    Create a command line parser to handle user actions for geometries.
    :return: a command line parser object
    """
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    set_subparser_obj = add_subparser(subparsers)

    return parser
