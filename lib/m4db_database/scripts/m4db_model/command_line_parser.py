from argparse import ArgumentParser

import m4db_database.configuration


def add_common_subparser_args(subparser):
    r"""
    Add some common arguments for each subparser.
    :param subparser:
    :return:
    """
    config = m4db_database.configuration.read_config_from_environ()

    # Set config
    software = config["m4db_serverside"]["default_micromag_software"]
    software_version = config["m4db_serverside"]["default_micromag_software_version"]

    subparser.add_argument("--software", default=software, type=str,
                           help="override the current micromagnetics software (default: {})".format(software))
    subparser.add_argument("--software-version", default=software_version, type=str,
                           help="override the current micromagnetics software version (default: {})".format(
                               software_version))

    # If ss_config was found ...
    db_user = config["m4db_serverside"]["default_m4db_user"]
    project = config["m4db_serverside"]["default_m4db_project"]
    subparser.add_argument("--db-user", default=db_user,
                           help="override the default m4db user (default: '{}')".format(db_user))
    subparser.add_argument("--project", default=project,
                           help="override the default m4db project (default: '{}')".format(project))


def add_from_json_subparser(subparsers):
    r"""
    Add subparser to deal with adding new models to m4db.
    :param subparsers: the subparsers objects.
    :return: the "add-from-json" subparser.
    """
    subparser = subparsers.add_parser(
        "add-from-json",
        help="Adds a new model or models to m4db."
    )

    subparser.add_argument("--max-evals", type=int,
                           help="the maximum no. of energy evaluations for the model",
                           default=100000)
    subparser.add_argument("--reps", type=int,
                           help="the number of repetitions per model entry",
                           default=1)
    subparser.add_argument("--json-file",
                           help="a JSON file containing model information to add to m4db (otherwise use stdin).")

    add_common_subparser_args(subparser)

    return subparser


def add_uid_list_subparser(subparsers):
    r"""
    Add a subparser to deal with querying models.
    :param subparsers:  the subparsers object.
    :return: the 'uid-list' subparser.
    """
    subparser = subparsers.add_parser(
        "uid-list",
        help="Retrieve a list of unique ids matching search criteria."
    )

    subparser.add_argument("--running-status",
                           default="finished",
                           choices=["not-run", "re-run", "running", "finished", "crashed", "any"],
                           help="schedule models with this running status")
    subparser.add_argument("--geometry",
                           help="the name of the geometry to execute")
    subparser.add_argument("--size",
                           type=float,
                           help="the size of the geometry")
    subparser.add_argument("--size-unit",
                           default="um",
                           choices=["m", "cm", "mm", "um", "nm", "pm", "fm", "am"],
                           help="the size unit for the geometry")
    subparser.add_argument("--size-convention",
                           default="ESVD",
                           choices=["ESVD", "ECVL"],
                           help="the size convention for the geometry")
    subparser.add_argument("--material",
                           help="a material belonging to the model")
    subparser.add_argument("--temperature",
                           help="a temperature belonging to the model")

    add_common_subparser_args(subparser)

    return subparser


def add_archive_subparser(subparsers):
    r"""
    Add a subparser to deal with archiving models.
    :param subparsers: the subparsers object.
    :return: the 'archive' subparser.
    """
    subparser = subparsers.add_parser(
        "archive",
        help="Archive the model with the given unique ID."
    )

    subparser.add_argument("unique_id", help="unique ID of a model.")

    add_common_subparser_args(subparser)

    return subparser


def command_line_parser():
    r"""
    Create a command line parser to handle model actions.
    :return: a command line parser
    """
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    add_from_json_subparser(subparsers)
    add_uid_list_subparser(subparsers)
    add_archive_subparser(subparsers)

    return parser
