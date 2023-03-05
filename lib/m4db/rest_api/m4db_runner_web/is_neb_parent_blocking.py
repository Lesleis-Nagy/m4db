r"""
An API call that will retrieve the parent dependency associated with an NEB.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def is_neb_parent_blocking(unique_id):
    r"""
    Retrieve whether the parent is blocking the execution of this NEB. If
    False, then either the NEB associated with this `unique_id` is finished
    or the NEB associated with this `unique_id` has no parent. If True, then
    the NEB associated with this `unique_id` has a parent and that parent
    is not in a 'finished' state.
    :param unique_id: the unique ID of an NEB.
    :return: True if the parent is in a blocking state, i.e. preventing
             the NEB with this unique ID from executing, otherwise False.
    """
    config = read_config_from_environ()
    protocol = config["m4db_runner_web"]["protocol"]
    host = config["m4db_runner_web"]["host"]
    port = config["m4db_runner_web"]["port"]

    service_url = f"{protocol}://{host}:{port}/is_neb_parent_blocking/{unique_id}"
    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)
    return output["return"]
