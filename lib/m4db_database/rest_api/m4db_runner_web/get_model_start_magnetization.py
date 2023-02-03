r"""
An API call that will retrieve whether a model has a parent.
"""

import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def get_model_start_magnetization(unique_id):
    r"""
    Retrieve start magnetization information about a model.
    :param unique_id: the unique ID of a model.
    :return: start magnetization information about a model.
    """
    config = read_config_from_environ()
    protocol = config["m4db_runner_web"]["protocol"]
    host = config["m4db_runner_web"]["host"]
    port = config["m4db_runner_web"]["port"]

    service_url = f"{protocol}://{host}:{port}/get_model_start_magnetization/{unique_id}"
    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)
    return output["return"]
