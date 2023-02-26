r"""
An API call that will set a model's quants values.
"""

import copy
import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


from m4db_database.rest.m4db_runner_web.set_model_quants import SetModelQuantsJSONSchema

def set_model_quants(unique_id, **kwargs):
    r"""
    Sets the model quants from kwargs.
    :param unique_id: the unique id of a model.
    :param kwargs: quant arguments.
    :return:
    """
    config = read_config_from_environ()

    quants = SetModelQuantsJSONSchema(kwargs)
    quants.unique_id = unique_id
    quants.validate()

    session = get_session()
    response = session.post(
        f"{config.runner_web.host}:{config.runner_web.port}/set-model-quants", json=json.dumps(quants.to_primitive()))
    response.raise_for_status()
