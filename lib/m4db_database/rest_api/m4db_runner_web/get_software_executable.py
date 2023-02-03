r"""
An API call that will retrieve the micromagnetics executable.
"""

import json

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def get_software_executable(name, version):
    r"""
    Retrieve the software executable.
    :param name: the name of the software.
    :param version: the version of the software.
    :return: None.
    """
    config = read_config_from_environ()
    service_url = "http://{host:}:{port:}/get_software_executable/{name:}/{version:}".format(
        host=config["m4db_runner_web"]["host"],
        port=config["m4db_runner_web"]["port"],
        name=name,
        version=version
    )
    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
