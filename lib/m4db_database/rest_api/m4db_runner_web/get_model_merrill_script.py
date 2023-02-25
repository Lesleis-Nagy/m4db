r"""
An API call that will retrieve a MERRILL model scripts.
"""

import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def get_model_merrill_script(unique_id, output_file):
    r"""
    Retrieve a MERRILL scripts that may be used to run a model.
    :param unique_id: the unique ID of a model.
    :param output_file: the destination to which the MERRILL scripts is saved.
    :return: None.
    """

    config = read_config_from_environ()
    session = get_session()
    response = session.get(
        f"{config.runner_web.host}:{config.runner_web.port}/get-model-merrill-script/{unique_id}")
    response.raise_for_status()

    output = json.loads(response.text)

    with open(output_file, "w") as fout:
        fout.write(output["return"])
