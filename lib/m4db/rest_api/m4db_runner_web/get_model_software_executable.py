r"""
An API call that will retrieve the software executable associated with a Model.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def get_model_software_executable(unique_id):
    r"""
    Retrieve the executable that will be used to run a model.
    :param unique_id: the unique ID of a model.
    :return: None.
    """
    config = read_config_from_environ()
    session = get_session()
    response = session.get(
        f"{config.runner_web.host}:{config.runner_web.port}/get-model-software-executable/{unique_id}")

    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
