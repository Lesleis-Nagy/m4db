from argparse import ArgumentParser

import m4db.configuration


def add_common_subparser_args(subparser):
    r"""
    Add some common arguments for each subparser.
    :param subparser:
    :return:
    """
    config = m4db.configuration.read_config_from_environ()

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


def add_fs_path_subparser(subparsers):
    r"""
    Add subparser to deal with adding new Fabian/Shcherbakov initial paths.
    :param subparsers: the subparsers object.
    :return: the "add-fs-path" sub parser.
    """
    subparser = subparsers.add_parser(
        "add-fs-path",
        help="Adds a new fs NEB path to m4db"
    )

    subparser.add_argument("model_unique_id_one", help="the first model part of a path")
    subparser.add_argument("model_unique_id_two", help="the second model part of a path")
    subparser.add_argument("--no-of-points", type=int, default=100, help="no. of points")
    subparser.add_argument("--max-energy-evaluations", type=int, help="max no. of energy evaluations")
    subparser.add_argument("--max-path-evaluations", type=int, help="max no. of path evaluations")
    subparser.add_argument("--external-field-x", type=float, help="external field x-component")
    subparser.add_argument("--external-field-y", type=float, help="external field y-component")
    subparser.add_argument("--external-field-z", type=float, help="external field z-component")
    subparser.add_argument("--external-field-strength", type=float, help="external field strength")
    subparser.add_argument("--external-field-unit",
                           default="mT", choices=["T", "mT", "uT", "nT"],
                           help="external field unit")

    add_common_subparser_args(subparser)
    return subparser


def add_neb_child_path_subparser(subparsers):
    r"""
    Add subparser to deal with adding child NEB paths to m4db.
    :param subparsers: the subparsers object.
    :return: the "add-child-path" sub parser
    """
    subparser = subparsers.add_parser(
        "add-neb-child-path",
        help="Adds a new NEB child path to m4db"
    )

    subparser.add_argument("parent_unique_id", help="the first model part of a path")
    subparser.add_argument("--spring-constant", type=float, help="spring constant")
    subparser.add_argument("--curvature-weight", type=float, help="curvature weight")
    subparser.add_argument("--no-of-points", type=int, default=100, help="no. of points")
    subparser.add_argument("--max-energy-evaluations", type=int, help="max no. of energy evaluations")
    subparser.add_argument("--max-path-evaluations", type=int, help="max no. of path evaluations")
    subparser.add_argument("--use-parent-external-field", action="store_true", help="if set then use the parent's external field.")
    subparser.add_argument("--external-field-x", type=float, help="external field x-component")
    subparser.add_argument("--external-field-y", type=float, help="external field y-component")
    subparser.add_argument("--external-field-z", type=float, help="external field z-component")
    subparser.add_argument("--external-field-strength", type=float, help="external field strength")
    subparser.add_argument("--external-field-unit",
                           default="mT", choices=["T", "mT", "uT", "nT"],
                           help="external field unit")

    add_common_subparser_args(subparser)
    return subparser


def add_fs_path_with_neb_child_subparser(subparsers):
    r"""
    Add a subparser to deal with adding a child with a parent path to m4db.
    :param subparsers: the subparsers object.
    :return: the 'add-fs-path-with-neb-child' sub parser
    """
    subparser = subparsers.add_parser(
        "add-fs-path-with-neb-child",
        help="Adds a new NEB Fabian/Shcherbakov path with an NEB child to m4db"
    )

    subparser.add_argument("model_unique_id_one", help="the first model part of a path")
    subparser.add_argument("model_unique_id_two", help="the second model part of a path")
    subparser.add_argument("--spring-constant", type=float, help="spring constant")
    subparser.add_argument("--curvature-weight", type=float, help="curvature weight")
    subparser.add_argument("--no-of-points", type=int, default=100, help="no. of points")
    subparser.add_argument("--max-energy-evaluations", type=int, help="max no. of energy evaluations")
    subparser.add_argument("--max-path-evaluations", type=int, help="max no. of path evaluations")
    subparser.add_argument("--external-field-x", type=float, help="external field x-component")
    subparser.add_argument("--external-field-y", type=float, help="external field y-component")
    subparser.add_argument("--external-field-z", type=float, help="external field z-component")
    subparser.add_argument("--external-field-strength", type=float, help="external field strength")
    subparser.add_argument("--external-field-unit",
                           default="mT", choices=["T", "mT", "uT", "nT"],
                           help="external field unit")
    subparser.add_argument("--force", action="store_true", help="disregard warnings and create the NEB")

    add_common_subparser_args(subparser)
    return subparser


def add_uid_list_subparser(subparsers):
    r"""
    Add the unique ID list subparser. This subparser deals with retreiving (filtered) NEB unique IDs.
    :param subparsers: the subparsers object
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


def command_line_parser():
    r"""
    Create a command line parser to handle neb actions.
    :return: a command line parser.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_fs_path_subparser(subparsers)
    add_neb_child_path_subparser(subparsers)
    add_fs_path_with_neb_child_subparser(subparsers)
    add_uid_list_subparser(subparsers)

    return parser
