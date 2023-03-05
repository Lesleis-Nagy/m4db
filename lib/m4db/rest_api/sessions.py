r"""
Create web sessions to communicate with web services.
"""

import requests

from requests.adapters import HTTPAdapter
from requests.adapters import Retry

from m4db.configuration import read_config_from_environ


def get_session():
    r"""
    Retrieve a web session object.
    :return: a web session object.
    """
    config = read_config_from_environ()

    session = requests.session()

    retries = Retry(
        total=config.runner_web.no_of_retries,
        backoff_factor=config.runner_web.backoff_factor,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))

    return session
