import json
import os
import falcon
import pandas

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database.file_io.merrill_stdio import extract_path_data

from m4db_database import global_vars


class GetNEBPathEnergiesCSV:
    r"""
    Retrieve the energy vs. index data associated with an NEB object.
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

        neb_stdout_file = os.path.join(
            config["file_root"],
            global_vars.neb_directory_name,
            uid_to_dir(unique_id),
            global_vars.neb_stdout_file_name
        )

        if os.path.exists(neb_stdout_file):
            path_data = extract_path_data(neb_stdout_file)
            df = pandas.DataFrame.from_dict(
                {"index": [r[0] for r in path_data],
                 "energy (J)": [r[1] for r in path_data]}
            )
            resp.content_type = "text/plain"
            resp.downloadable_as = "{}.csv".format(unique_id)
            resp.body = df.to_csv()
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
