r"""
Handle the creation/destruction of temporary directories.
"""

import shutil
import uuid

from m4db.utilities_logging import get_logger
from m4db.configuration import read_config_from_environ


def create_temporary_dir(req, resp, resource, params):
    config = read_config_from_environ()
    logger = get_logger()

    req.working_dir = config["m4db_serverside"]["working_dir"]

    req.temp_dir = os.path.join(
        req.working_dir, str(uuid.uuid4())
    )

    os.makedirs(req.temp_dir, exist_ok=True)

    logger.debug(f"created temporary directory {req.temp_dir}")


def remove_temporary_dir(req, resp, resource):
    logger = get_logger()
    shutil.rmtree(req.temp_dir)

    logger.debug(f"removed temporary directory {req.temp_dir}")