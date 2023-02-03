r"""
A service to retrieve all the possible running statues
"""
import falcon

import simplejson as json

from m4db_database.orm.latest import RunningStatus


class GetRunningStatuses:
    r"""
    Falcon service to retrieve model running statuses.
    """

    def on_get(self, req, resp):
        r"""
        Retrieve information about all the running statuses on the system.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :return: None
        """
        running_statuses = self.session.query(RunningStatus).all()

        if not running_statuses or len(running_statuses) == 0:
            resp.status = falcon.HTTP_404
            return

        response = []
        for running_status in running_statuses:
            response.append({
                "name": running_status.name,
                "description": running_status.description
            })

        resp.text = json.dumps(response)
