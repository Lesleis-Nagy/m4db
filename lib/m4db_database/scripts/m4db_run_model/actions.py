r"""
A selection of actions that will execute a model.
"""
from m4db_database.utilities_logging import get_logger

import m4db_database.runner.model.run_model as ssrunner

from m4db_database.rest_api.m4db_runner_web.set_model_running_status import set_model_running_status


def run_model(args):
    r"""
    Run a model.
    :param args: program command line arguments.
    :return: None
    """
    logger = get_logger()
    try:
        ssrunner.run_model(args.unique_id)
    except Exception as e:
        logger.debug(str(e))
        set_model_running_status(args.unique_id, "crashed")
        raise e
