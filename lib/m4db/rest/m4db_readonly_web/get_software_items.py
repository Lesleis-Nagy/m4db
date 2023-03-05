r"""
A collection of Falcon services to retrieve software data.
"""
import falcon

import simplejson as json

from m4db.orm.schema import Software


class GetSoftwareItems:
    r"""
    Falcon service to retrieve all the software data managed by m4db.
    """

    def on_get(self, req, resp):
        r"""
        Retrieve software information.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :return: None
        """
        software_items = self.session.query(Software).all()

        if not software_items or len(software_items) == 0:
            resp.status = falcon.HTTP_404
            return

        response = []
        for software_item in software_items:
            response.append({
                "name": software_item.name,
                "version": software_item.version,
                "description": software_item.description
            })

        resp.body = json.dumps(response)
