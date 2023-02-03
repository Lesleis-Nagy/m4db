r"""
A service to retrieve the start magnetization information of a model.
"""

import json

from m4db_database.orm.latest import Model
from m4db_database.orm.latest import UniformField
from m4db_database.orm.latest import RandomField
from m4db_database.orm.latest import ModelField


class GetModelStartMagnetization:

    def on_get(self, req, resp, unique_id):
        r"""
        Return information about the start model/field of a model with the given unique ID.
        :param req: the request object.
        :param resp: the response object.
        :param unique_id: the unique identifier of a model.
        :return: None
        """
        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one()

        return_value = {}
        if isinstance(model.start_magnetization, UniformField):
            return_value = {
                "type": "uniform",
                "dir_x": model.start_magnetization.dir_x,
                "dir_y": model.start_magnetization.dir_y,
                "dir_z": model.start_magnetization.dir_z
            }
        elif isinstance(model.start_magnetization, RandomField):
            return_value = {
                "type": "random"
            }
        elif isinstance(model.start_magnetization, ModelField):
            return_value = {
                "type": "model",
                "unique_id": model.start_magnetization.model.unique_id,
                "running_status": model.start_magnetization.model.running_status.name
            }
        else:
            ValueError("Unknown field type when attempting to retrieve start magnetization")

        resp.text = json.dumps({"return": return_value})
