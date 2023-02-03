r"""
Create a command line parser to handle input for a model runner utility scripts.
"""

from argparse import ArgumentParser


def command_line_parser():
    r"""
    Create a command line parser to handle NEB runner actions.
    :return: a command line parser.
    """
    parser = ArgumentParser()

    parser.add_argument("unique_id", help="the unique ID of the NEB to run")

    return parser
