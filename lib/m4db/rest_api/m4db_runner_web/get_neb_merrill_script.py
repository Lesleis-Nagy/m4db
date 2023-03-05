r"""
An API call that will retrieve MERRILL neb scripts.
"""

import json

from m4db.configuration import read_config_from_environ

from m4db.rest_api.sessions import get_session


def get_neb_merrill_script(unique_id, output_file):
    r"""
    Retreive a MERRILL scripts that may be used to an NEB.
    :param unique_id: the unique ID of an NEB.
    :param output_file: the destination to which the MERRILL scripts is saved.
    :return: None.
    """
    config = read_config_from_environ()
    service_url = "http://{host:}:{port:}/get_neb_merrill_script/{unique_id:}".format(
        host=config["m4db_runner_web"]["host"],
        port=config["m4db_runner_web"]["port"],
        unique_id=unique_id
    )
    session = get_session()
    response = session.get(service_url)
    response.raise_for_status()

    output = json.loads(response.text)
    with open(output_file, "w") as fout:
        fout.write(output["return"])
