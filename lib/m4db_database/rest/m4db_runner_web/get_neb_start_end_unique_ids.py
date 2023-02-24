r"""
A service to retrieve the start/end unique ids associated with an NEB.
"""

import json

from m4db_database.orm.schema import NEB


class GetNebStartEndUniqueIds:

    def on_get(self, req, resp, unique_id):
        r"""
        Get the unique IDs associated with the path start/end models of the NEB
        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of an NEB
        :return: None
        """
        neb = self.session.query(NEB).\
            filter(NEB.unique_id == unique_id).one()

        resp.body = json.dumps(
            {
                "return": {
                    "start_unique_id": neb.start_model.unique_id,
                    "end_unique_id": neb.end_model.unique_id
                }
            }
        )
