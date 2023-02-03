r"""
Create a command line parser to handle input for NEB scheduler utility scripts.
"""

from argparse import ArgumentParser


def command_line_parser():
    r"""
    Create a command line parser to handle NEB scheduler actions.
    :return:  a command line parser.
    """
    parser = ArgumentParser()

    parser.add_argument("--running-status",
                        default="not-run",
                        choices=["not-run", "re-run", "running", "finished", "crashed", "any"],
                        help="schedule NEBs with this running status")
    parser.add_argument("--geometry",
                        help="the name of the geometry to execute")
    parser.add_argument("--size",
                        type=float,
                        help="the size of the geometry")
    parser.add_argument("--size-unit",
                        default="um",
                        choices=["m", "cm", "mm", "um", "nm", "pm", "fm", "am"],
                        help="the size unit for the geometry")
    parser.add_argument("--size-convention",
                        default="ESVD",
                        choices=["ESVD", "ECVL"],
                        help="the size convention for the geometry")
    parser.add_argument("--db-user",
                        help="the database user to which NEBs belong")
    parser.add_argument("--software",
                        help="the software that the NEB should be run with")
    parser.add_argument("--software-version",
                        help="the version of the software that the NEB should be run with")
    parser.add_argument("--material",
                        help="a material belonging to the NEB")
    parser.add_argument("--temperature",
                        help="a temperature belonging to the NEB")
    parser.add_argument("--real-run",
                        action="store_true",
                        help="actually schedule the NEBs.")
    parser.add_argument("--list-unique-ids",
                        action="store_true",
                        help="list out the unique ids of the NEBs being scheduled.")
    parser.add_argument("--limit", type=int,
                        help="set a limit on the number of NEBs scheduled.")

    return parser

