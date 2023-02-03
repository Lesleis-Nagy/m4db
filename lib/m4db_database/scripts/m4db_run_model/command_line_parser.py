r"""
Create a command line parser to handle input for a model runner utility scripts.
"""

from argparse import ArgumentParser


def command_line_parser():
    r"""
    Create a command line parser to handle model runner actions.
    Returns: a command line parser
    """
    parser = ArgumentParser()

    parser.add_argument("unique_id", help="The unique ID of the model to run")

    return parser
