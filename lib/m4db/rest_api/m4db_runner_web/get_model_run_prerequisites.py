r"""
A wrapper API that will communicate with the web server in order to retrieve model run prerequisite data.
"""
import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def get_model_run_prerequisites(unique_id: str):
    r"""
    Retrieve a model's prerequisite magnetization data.

    :param unique_id: the model's unique id.

    :return: a dictionary with the following keys:
                1) merrill-script - a string holding the contents of the merrill script that will run this model.
                2) geometry-file-abs-path - the absolute path to the geometry that this model requires.
                3) model-dir-abs-pat - the model's destination directory.
                4) merrill-executable - the merrill executable needed to run the `merrill-script`.
    """

    config = read_config_from_environ()

    session = get_session()

    response = session.get(
        f"{config.runner_web.host}:{config.runner_web.port}/get-model-run-prerequisites/{unique_id}"
    )

    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
