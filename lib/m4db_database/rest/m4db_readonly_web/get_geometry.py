r"""
A collection of services to retrieve geometry information.
"""
import falcon

import simplejson as json

from m4db_database.orm.latest import Geometry
from m4db_database.orm.latest import Unit
from m4db_database.orm.latest import SizeConvention


class GetAllGeometryNames:
    r"""
    Falcon service to retrieve unique geometry names.
    """

    def on_get(self, req, resp):
        r"""
        Retrive information about all geometry names.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :return: None
        """

        records = self.session.query(Geometry.name, Geometry.description).distinct().all()
        response = [
            {
                "name": record[0],
                "description": record[1]
            }
            for record in records
        ]

        if not records or len(records) == 0:
            resp.status = falcon.HTTP_404
            return

        resp.text = json.dumps(response)


class GetGeometrySizes:
    r"""
    Falcon service to retrieve all the sizes available to a specific geometry name.
    """

    def on_get(self, req, resp, geometry_name):
        r"""
        Retrieve all the sizes available to a geometry.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :param geometry_name: The name of a geometry
        :return: None
        """

        records = self.session.query(Geometry.size, Unit.symbol, SizeConvention.symbol).\
            join(Unit, Geometry.size_unit_id == Unit.id).\
            join(SizeConvention, Geometry.size_convention_id == SizeConvention.id).\
            filter(Geometry.name == geometry_name).\
            distinct().all()

        if not records or len(records) == 0:
            resp.status = falcon.HTTP_404
            return

        response = [
            {
                "size": record[0],
                "unit": record[1],
                "convention": record[2]
            }
            for record in records
        ]

        resp.text = json.dumps(response)
