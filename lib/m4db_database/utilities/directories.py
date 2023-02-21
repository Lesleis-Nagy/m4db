r"""
A collection of utility routines for m4db directories.
"""

import os

from m4db_database.utilities.unique_id import uid_to_dir
from m4db_database.configuration import read_config_from_environ

from m4db_database import GLOBAL

def geometry_directory(unique_id):
    r"""
    Retrieve the geometry directory associated with the input unique id.
    Args:
        unique_id:

    Returns: The M4DB directory containing the geometry path.
    """
    config = read_config_from_environ()

    dest_dir = os.path.join(
        config.database.file_root,
        GLOBAL.geometry_directory_name,
        uid_to_dir(unique_id)
    )

    return dest_dir
