r"""
An API call that will set a model's quants values.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session

from m4db.rest.m4db_runner_web.set_model_running_status import SetModelRunningStatusJSONSchema


def set_model_running_status(unique_id, running_status):
    r"""
    Sets the model quants from kwargs.
    :param unique_id: the unique id of a model.
    :param running_status: the new model running status.
    :return: None
    """
    config = read_config_from_environ()

    new_status = SetModelRunningStatusJSONSchema()
    new_status.unique_id = unique_id
    new_status.new_running_status = running_status

    session = get_session()
    response = session.post(
        f"{config.runner_web.host}:{config.runner_web.port}/set-model-running-status",
        json=json.dumps(new_status.to_primitive())
    )

    response.raise_for_status()
