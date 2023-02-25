r"""
A service to set a model's running status.
"""
import falcon
import json

from m4db_database import GLOBAL
from m4db_database.orm.schema import RunningStatus
from m4db_database.orm.schema import RunningStatusEnum

from m4db_database.orm.schema import Model

import schematics
import schematics.exceptions

from m4db_database.utilities.logger import get_logger


class SetModelRunningStatusJSONSchema(schematics.models.Model):
    unique_id = schematics.types.StringType(regex=GLOBAL.UID_REGEX,
                                            deserialize_from="unique-id",
                                            serialized_name="unique-id",
                                            required=True)
    new_running_status = schematics.types.StringType(choices=[RunningStatusEnum.not_run.value,
                                                              RunningStatusEnum.re_run.value,
                                                              RunningStatusEnum.running.value,
                                                              RunningStatusEnum.finished.value,
                                                              RunningStatusEnum.crashed.value,
                                                              RunningStatusEnum.scheduled.value],
                                                     deserialize_from="new-running-status",
                                                     serialized_name="new-running-status",
                                                     required=True)

class SetModelRunningStatus:
    def on_post(self, req, resp):
        r"""
        Set a model's running status.

        :param req: request object.
        :param resp: response object.

        :return: none
        """

        parameters = req.media
        self.logger.info(parameters)

        try:
            running_status_data = SetModelRunningStatusJSONSchema(json.loads(parameters))
            running_status_data.validate()
            self.logger.info(f"running-status-data: {running_status_data.to_primitive()}")

        except schematics.exceptions.ValidationError as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            return
        except schematics.exceptions.DataError as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            return

        # Retrieve the running status ID.
        new_running_status = self.session.query(RunningStatus).\
            filter(RunningStatus.name == running_status_data.new_running_status).one()

        # Retrieve the model and set the running status id.
        model = self.session.query(Model).\
            filter(Model.unique_id == running_status_data.unique_id).one_or_none()
        if model is None:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({
                "error": f"Missing unique id: '{running_status_data.unique_id}'."
            })
            return

        model.running_status = new_running_status
        self.session.commit()
