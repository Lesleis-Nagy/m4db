r"""
A service to generate a scripts to retrieve a model's running status.
"""
import falcon

import json

from m4db.orm.schema import Model


class GetModelRunningStatus:

    def on_get(self, req, resp, unique_id):
        r"""
        Get a model's running status.
        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of a model.
        :return: None
        """
        # Retrieve the model.
        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one_or_none()

        if model is None:
            resp.status = falcon.HTTP_404
            return
        else:
            resp.text = json.dumps({"return": model.running_status.name})
            return
