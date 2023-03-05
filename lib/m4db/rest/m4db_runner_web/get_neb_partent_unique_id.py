r"""
A service to check if an NEB path has a parent or not.
"""

import json

from m4db.orm.schema import NEB


class GetNEBParentUniqueId:

    def on_get(self, req, resp, unique_id):
        r"""
        Return the unique id of the parent of the NEB (if it exists).
        :param req: the request object.
        :param resp: the response object.
        :param unique_id: the unique identifier of an NEB.
        :return: None
        """
        neb = self.session.query(NEB).\
            filter(NEB.unique_id == unique_id).one()

        if neb.parent_neb is None:
            # The NEB is parentless.
            return_value = None
        else:
            return_value = neb.parent_neb.unique_id

        resp.text = json.dumps({"return": return_value})
