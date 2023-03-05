r"""
An API call that will retrieve a model's running status.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def get_model_running_status(unique_id):
    r"""
    Retrieve a model's running status.

    :param unique_id: the unique identifier of a model.

    :return: the running status of the model.

    """
    config = read_config_from_environ()
    session = get_session()
    response = session.get(
        f"{config.runner_web.host}:{config.runner_web.port}/get-model-running-status/{unique_id}"
    )
    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
