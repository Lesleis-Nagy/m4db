r"""
A collection of Falcon web services to retrieve NEB data.
"""

import io
import mimetypes
import os

import falcon

from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database import GLOBAL


class GetAllNEBDataZip:
    r"""
    Falcon service to retrieve NEB data file as a zipped object.
    """
    def on_get(self, req, resp, unique_id):
        r"""
        Retrieve the 'data.zip' associated with an NEB object that has the given Unique ID.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :param unique_id: unique identifier of the NEB.
        :return: None
        """
        # Check that the data exists.
        data_zip = os.path.join(
            self.config["file_root"],
            GLOBAL.neb_directory_name,
            uid_to_dir(unique_id),
            GLOBAL.data_zip
        )

        if not os.path.isfile(data_zip):
            resp.status = falcon.HTTP_404
            return
        else:
            self.logger.debug(f"returning zip file '{data_zip}'")
            resp.content_type = mimetypes.guess_type(data_zip)[0]
            resp.stream = io.open(data_zip, "rb")
            resp.content_length = os.path.getsize(data_zip)
            return
