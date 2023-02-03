r"""
An API call that will retrieve whether an NEB has a parent.
"""

import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def get_neb_parent_unique_id(unique_id):
    r"""
    Retrieve the unique ID of the parent of an NEB.
    :param unique_id: the unique ID of an NEB.
    :return: The unique ID of the parent of this NEB, otherwise None.
    """
    config = read_config_from_environ()
    protocol = config["m4db_runner_web"]["protocol"]
    host = config["m4db_runner_web"]["host"]
    port = config["m4db_runner_web"]["port"]

    service_url = f"{protocol}://{host}:{port}/get_neb_parent_unique_id/{unique_id}"
    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)
    return output["return"]
