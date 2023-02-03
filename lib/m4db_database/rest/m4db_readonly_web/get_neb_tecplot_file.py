r"""
A service to retrieve a tecplot NEB file
"""

r"""
A collection of Falcon web services to retrieve NEB data.
"""
import os
import falcon
import pandas

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database import global_vars


class GetNebTecplotFile:
    r"""
    Falcon service to retrieve NEB path Tecplot files.
    """

    def on_get(self, req, resp, unique_id):
        r"""
        Retrieve the information associated with an NEB object that has
        the given unique id.

        :param req: the Falcon request object.
        :param resp: the Falcon response object
        :param unique_id: the unique identifier of the NEB.
        """
        config = read_config_from_environ()

        neb_path_file = os.path.join(
            config["file_root"],
            global_vars.neb_directory_name,
            uid_to_dir(unique_id),
            global_vars.neb_tecplot_file_name
        )

        if os.path.exists(neb_path_file):
            resp.content_type = "text/plain"
            resp.downloadable_as = "{}.tec".format(unique_id)
            with open(neb_path_file, "r") as fout:
                resp.body = fout.read()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
