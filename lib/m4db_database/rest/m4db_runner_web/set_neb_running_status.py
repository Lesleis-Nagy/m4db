r"""
A Service to set an NEB's running status.
"""

from m4db_database.orm.schema import RunningStatus
from m4db_database.orm.schema import NEB


class SetNEBRunningStatus:
    def on_post(self, req, resp):
        r"""
        Set an NEB's running status.
        :param req: request object.
        :param resp: response object.
        :return: none
        """

        parameters = req.media

        # Retrieve the running status ID.
        running_status_id, = self.session.query(RunningStatus.id).\
            filter(RunningStatus.name == parameters["running_status"]).one()

        # Retrieve the NEB and set the running status id.
        neb = self.session.query(NEB).\
            filter(NEB.unique_id == parameters["unique_id"]).one()
        neb.running_status_id = running_status_id
        self.session.commit()
