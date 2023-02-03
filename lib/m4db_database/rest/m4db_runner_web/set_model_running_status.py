r"""
A service to set a model's running status.
"""

from m4db_database.orm.latest import RunningStatus
from m4db_database.orm.latest import Model


class SetModelRunningStatus:
    def on_post(self, req, resp):
        r"""
        Set a model's running status.
        :param req: request object.
        :param resp: response object.
        :return: none
        """

        parameters = req.media

        # Retrieve the running status ID.
        running_status_id, = self.session.query(RunningStatus.id).\
            filter(RunningStatus.name == parameters["running_status"]).one()

        # Retrieve the model and set the running status id.
        model = self.session.query(Model).\
            filter(Model.unique_id == parameters["unique_id"]).one()
        model.running_status_id = running_status_id
        self.session.commit()
