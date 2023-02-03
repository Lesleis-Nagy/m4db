r"""
An API call that will set a model's quants values.
"""

import copy
import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def set_model_quants(unique_id, **kwargs):
    r"""
    Sets the model quants from kwargs.
    :param unique_id: the unique id of a model.
    :param kwargs: quant arguments.
    :return:
    """
    config = read_config_from_environ()
    service_url = "http://{host:}:{port:}/set_model_quants".format(
        host=config["m4db_runner_web"]["host"],
        port=config["m4db_runner_web"]["port"]
    )

    params = copy.deepcopy(kwargs)
    params["unique_id"] = unique_id
    session = get_session()
    response = session.post(service_url, data=json.dumps(params))
    response.raise_for_status()

