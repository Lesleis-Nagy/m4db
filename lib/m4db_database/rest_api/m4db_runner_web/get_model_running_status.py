r"""
An API call that will retrieve a model's running status.
"""

import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def get_model_running_status(unique_id):
    r"""
    Retrieve a model's running status.
    :param unique_id: the unique identifier of a model.
    :return: the running status of the model.
    """
    config = read_config_from_environ()
    service_url = "http://{host:}:{port:}/get_model_running_status/{unique_id:}".format(
        host=config["m4db_runner_web"]["host"],
        port=config["m4db_runner_web"]["port"],
        unique_id=unique_id
    )
    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
