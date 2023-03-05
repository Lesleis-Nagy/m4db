r"""
A collection of utility routines for m4db directories.
"""

import os

from m4db.utilities.unique_id import uid_to_dir
from m4db.configuration import read_config_from_environ

from m4db import GLOBAL

def geometry_directory(unique_id):
    r"""
    Retrieve the geometry directory associated with the input unique id.
    Args:
        unique_id: the geometry unique id.

    Returns: The M4DB directory containing the geometry path.
    """
    config = read_config_from_environ()

    dest_dir = os.path.join(
        config.database.file_root,
        GLOBAL.GEOMETRY_DIRECTORY_NAME,
        uid_to_dir(unique_id)
    )

    return dest_dir


def model_directory(unique_id):
    r"""
    Retrieve the model directory associated with the input unique id.
    Args:
        unique_id: the model unique id.

    Returns: the M4DB directory containing the model path.

    """
    # This is the final destination of model data.

    config = read_config_from_environ()

    dest_dir = os.path.join(
        config.database.file_root,
        GLOBAL.MODEL_DIRECTORY_NAME,
        uid_to_dir(unique_id)
    )

    return dest_dir
