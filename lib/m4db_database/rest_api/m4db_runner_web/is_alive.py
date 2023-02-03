r"""
An API call that will check to see whether the m4db runner web service is is_alive.
"""

from m4db_database.configuration import read_config_from_environ

from m4db_database.rest_api.sessions import get_session


def is_alive():
    r"""
    Wrapper function to communicate with m4db-runner-web to test whether the service is running and accessible.
    :return: True if `m4db-runner-web` is accessible, otherwise False.
    """
    config = read_config_from_environ()
    service_url = "http://{host:}:{port:}/is_alive".format(
        host=config["m4db_runner_web"]["host"],
        port=config["m4db_runner_web"]["port"]
    )
    session = get_session()
    try:
        response = session.get(service_url)
        response.raise_for_status()
    except:
        return False
    return True
