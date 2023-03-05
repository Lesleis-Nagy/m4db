r"""
An API call that will retrieve the start/end model unique IDs associated with an NEB path.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def get_neb_start_end_unique_ids(unique_id):
    r"""
    Retrieve the model start/end unique IDs associated with the NEB path.
    :param unique_id: the unique ID of an NEB.
    :return: the start/end model unique IDs associated with this NEB.
    """
    config = read_config_from_environ()

    protocol = config["m4db_runner_web"]["protocol"]
    host = config["m4db_runner_web"]["host"]
    port = config["m4db_runner_web"]["port"]

    service_url = f"{protocol}://{host}:{port}/get_neb_start_end_unique_ids/{unique_id}"

    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]["start_unique_id"], output["return"]["end_unique_id"]
