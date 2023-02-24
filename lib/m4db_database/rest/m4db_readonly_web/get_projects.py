r"""
A service to retrieve all the projects on m4db.
"""
import falcon

import simplejson as json

from m4db_database.orm.schema import Project


class GetProjects:
    r"""
    Falcon service to retrieve projects.
    """

    def on_get(self, req, resp):
        r"""
        Retrieve project information.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :return:
        """
        projects = self.session.query(Project).all()

        if not projects or len(projects) == 0:
            resp.status = falcon.HTTP_404
            return

        response = []
        for project in projects:
            response.append({
                "name": project.name,
                "description": project.description
            })

        resp.body = json.dumps(response)
