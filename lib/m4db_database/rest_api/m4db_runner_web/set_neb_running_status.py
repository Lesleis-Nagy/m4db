r"""
An API call that will set an NEB's running status.
"""

import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def set_neb_running_status(unique_id, running_status):
    r"""
    Sets the model quants from kwargs.
    :param unique_id: the unique id of an NEB.
    :param running_status: the new NEB running status.
    :return: None
    """
    config = read_config_from_environ()
    service_url = "http://{host:}:{port:}/set_neb_running_status".format(
        host=config["m4db_runner_web"]["host"],
        port=config["m4db_runner_web"]["port"]
    )

    session = get_session()
    response = session.post(service_url, data=json.dumps({"unique_id": unique_id, "running_status": running_status}))
    response.raise_for_status()
