r"""
A service to retrieve the parental-blocking status of an NEB
"""

import json

from m4db.orm.schema import NEB


class IsNEBParentBlocking:

    def on_get(self, req, resp, unique_id):
        r"""
        Get the parent blocked status of an NEB.
        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of an NEB
        :return: None
        """
        neb = self.session.query(NEB).\
            filter(NEB.unique_id == unique_id).one()

        if neb.parent_neb is None:
            # If the NEB has no parent then it cannot be blocked by the parent.
            return_value = False
        else:
            # There is a parent.
            if neb.parent_neb.running_status.name == "finished":
                # The parent is finished and so no longer blocks.
                return_value = False
            else:
                # The parent has some status other than finished and so it blocks.
                return_value = True

        resp.text = json.dumps({"return": return_value})
