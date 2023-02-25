r"""
A service to retrieve the start magnetization information of a model.
"""
import falcon
import json

from m4db_database.orm.schema import Model
from m4db_database.orm.schema import UniformInitialMagnetization
from m4db_database.orm.schema import RandomInitialMagnetization
from m4db_database.orm.schema import ModelInitialMagnetization

from m4db_database.utilities.logger import get_logger

class GetModelStartMagnetization:

    def on_get(self, req, resp, unique_id):
        r"""
        Return information about the start model/field of a model with the given unique ID.

        :param req: the request object.
        :param resp: the response object.
        :param unique_id: the unique identifier of a model.

        :return: None
        """
        logger = get_logger()

        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one_or_none()

        if model is None:
            resp.status = falcon.HTTP_404
            return

        if isinstance(model.start_magnetization, UniformInitialMagnetization):
            return_value = {
                "type": "uniform",
                "dir-x": model.start_magnetization.dir_x,
                "dir-y": model.start_magnetization.dir_y,
                "dir-z": model.start_magnetization.dir_z
            }
        elif isinstance(model.start_magnetization, RandomInitialMagnetization):
            return_value = {
                "type": "random"
            }
        elif isinstance(model.start_magnetization, ModelInitialMagnetization):
            return_value = {
                "type": "model",
                "unique-id": model.start_magnetization.model.unique_id,
                "running-status": model.start_magnetization.model.running_status.name
            }
        else:
            logger.error("Unknown start magnetization type!")
            falcon.status = falcon.HTTP_500
            return

        print("Returning start magnetization.")
        resp.text = json.dumps({"return": return_value})
