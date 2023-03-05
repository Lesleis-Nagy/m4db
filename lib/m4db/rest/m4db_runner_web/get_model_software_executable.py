r"""
A service to retrieve the software executable associated with a model.
"""
import falcon

import json

from m4db.orm.schema import Model


class GetModelSoftwareExecutable:

    def on_get(self, req, resp, unique_id):
        r"""
        Get the executable associated with a model.
        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of a model.
        :return: None
        """
        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one_or_none()

        if model is None:
            resp.status = falcon.HTTP_404
            return
        else:
            resp.text = json.dumps({"return": model.mdata.software.executable})
            return