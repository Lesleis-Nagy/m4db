r"""
A service to retrieve a software's executable.
"""

import json
import falcon

from m4db_database.orm.schema import Software


class GetSoftware:

    def on_get(self, req, resp, name, version):
        r"""
        Get/generate a scripts retrieve the software executable.
        :param req: request object.
        :param resp: response object.
        :return: None
        """
        software = self.session.query(Software). \
            filter(Software.name == name). \
            filter(Software.version == version).one_or_none()

        if software is None:
            resp.status = falcon.HTTP_404
            return
        else:
            resp.text = json.dumps({"return": software.executable})
            return
