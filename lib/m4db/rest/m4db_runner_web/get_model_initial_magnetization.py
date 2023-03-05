r"""
A service to retrieve the start magnetization information of a model.
"""
import falcon
import json

from m4db.orm.schema import Model
from m4db.orm.schema import UniformInitialMagnetization
from m4db.orm.schema import RandomInitialMagnetization
from m4db.orm.schema import ModelInitialMagnetization


class GetModelInitialMagnetization:

    def on_get(self, req, resp, unique_id):
        r"""
        Return information about the start model/field of a model with the given unique ID.

        :param req: the request object.
        :param resp: the response object.
        :param unique_id: the unique identifier of a model.

        :return: None
        """

        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one_or_none()
        if model is None:
            resp.status = falcon.HTTP_404
            return

        self.logger.debug(f"Model id {unique_id}, checking instance of start magnetization.")
        if isinstance(model.initial_magnetization, UniformInitialMagnetization):
            self.logger.debug(f"Model id {unique_id}, starts with a uniformly magnetized state.")
            return_value = {
                "type": "uniform",
                "dir-x": model.initial_magnetization.dir_x,
                "dir-y": model.initial_magnetization.dir_y,
                "dir-z": model.initial_magnetization.dir_z
            }
        elif isinstance(model.initial_magnetization, RandomInitialMagnetization):
            self.logger.debug(f"Model id {unique_id}, starts with a randomly magnetized state.")
            return_value = {
                "type": "random"
            }
        elif isinstance(model.initial_magnetization, ModelInitialMagnetization):
            self.logger.debug(f"Model id {unique_id}, starts with a magnetized state based on an existing model.")
            return_value = {
                "type": "model",
                "unique-id": model.initial_magnetization.model.unique_id,
                "running-status": model.initial_magnetization.model.running_status.name
            }
        else:
            self.logger.error(f"Model id {unique_id}, unknown initial magnetization type!")
            falcon.status = falcon.HTTP_500
            return

        resp.text = json.dumps({"return": return_value})
