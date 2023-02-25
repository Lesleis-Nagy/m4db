r"""
A wrapper API that will communicate with the web server in order to retrieve initial magnetization data.
"""
import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def get_model_initial_magnetization(unique_id: str):
    r"""
    retrieve a model's initial magnetization data.

    :param unique_id: the model's unique id.

    :return: one of three types of dictionary:
                1) a uniform initial magnetization, with the following fields:
                    1.1) type is the type of the field, in this case it is always set to "uniform".
                    1.2) dir-x is the x direction of the magnetization field.
                    1.3) dir-y is the y direction of the magnetization field.
                    1.4) dir-z is the z direction of the magnetization field.
                    1.5) magnitude is the magnitude of the magnetization field (in micro Tesla).
                2) a python dictionary, with the following fields:
                    2.1) type is the type of the field, in this case it is always set to "model".
                    2.2) unique-id - the unique id of the parent.
                3) a python dictionary, with the following fields:
                    3.1) type is the type of the field, in this case it is always set to "random".
    """

    config = read_config_from_environ()

    session = get_session()

    response = session.get(
        f"{config.runner_web.host}:{config.runner_web.port}/get-model-initial-magnetization/{unique_id}"
    )

    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
