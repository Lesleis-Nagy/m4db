r"""
An API call that will retrieve the micromagnetics executable.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def get_software_executable(name, version):
    r"""
    Retrieve the software executable.

    :param name: the name of the software.
    :param version: the version of the software.

    :return: None.
    """
    config = read_config_from_environ()
    session = get_session()
    response = session.get(
        f"{config.runner_web.host}:{config.runner_web.port}/get-software-executable/{name}/{version}")

    response.raise_for_status()

    output = json.loads(response.text)

    return output["return"]
