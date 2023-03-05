r"""
A selection of actions that will execute a model.
"""
from m4db.utilities_logging import get_logger

import m4db.runner.neb.run_neb as ssrunner

from m4db.rest_api.m4db_runner_web.set_neb_running_status import set_neb_running_status


def run_neb(args):
    r"""
    Run an NEB
    :param args: program command line arguments.
    :return: None
    """
    logger = get_logger()
    try:
        ssrunner.run_neb(args.unique_id)
    except Exception as e:
        logger.debug(str(e))
        set_neb_running_status(args.unique_id, "crashed")
        raise e
