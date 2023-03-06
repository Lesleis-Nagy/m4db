r"""
A very simple service that can be used to check that m4db_runner_web is 'is_alive'.
"""

import falcon

from m4db.utilities.logger import get_logger

class IsAlive:
    r"""
    A REST service that may be used to test whether the server is is_alive.
    """

    def on_get(self, req, resp):
        r"""
        The 'get' http request handler.
        """
        logger = get_logger()
        logger.debug("This is the /is-alive service.")
        resp.status = falcon.HTTP_200
        return
