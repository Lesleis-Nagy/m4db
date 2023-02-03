r"""
A service to retrieve a software's executable.
"""

import json
import falcon

from m4db_database.orm.latest import Software


class GetSoftwareExecutable:

    def on_get(self, req, resp, name, version):
        r"""
        Get/generate a scripts retrieve the software executable.
        :param req: request object.
        :param resp: response object.
        :return: None
        """
        software = self.session.query(Software). \
            filter(Software.name == name). \
            filter(Software.version == version).one()

        if software.executable is None or software.executable == "":
            resp.status = falcon.HTTP_404
        else:
            resp.body = json.dumps({"return": software.executable})
