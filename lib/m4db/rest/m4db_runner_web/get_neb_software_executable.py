r"""
A service to retrieve the software executable associated with an NEB.
"""

import json

from m4db.orm.schema import NEB


class GetNEBSoftwareExecutable:

    def on_get(self, req, resp, unique_id):
        r"""
        Get the executable associated with an NEB.
        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of an NEB.
        :return: None
        """
        model = self.session.query(NEB).\
            filter(NEB.unique_id == unique_id).one()

        resp.body = json.dumps({"return": model.mdata.software.executable})

