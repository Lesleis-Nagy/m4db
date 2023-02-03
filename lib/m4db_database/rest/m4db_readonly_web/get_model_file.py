r"""
A collection of Falcon web services to retrieve model data.
"""

import io
import mimetypes
import os

import zipfile
import falcon

from falcon import before
from falcon import after

from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database import GLOBAL

from m4db_database.utilities.archive import unarchive_model

from m4db_database.rest.m4db_readonly_web.temporary_dirs import create_temporary_dir
from m4db_database.rest.m4db_readonly_web.temporary_dirs import remove_temporary_dir


class GetAllModelDataZip:
    r"""
    Falcon service to retrieve model data file as a zipped object.
    """
    def on_get(self, req, resp, unique_id):
        r"""
        Retrieve the 'data.zip' associated with a model object that has the given Unique ID.
        :param req: Falcon request object.
        :param resp: Falcon response object.
        :param unique_id: unique identifier of the model.
        :return: None
        """
        # Check that the data exists.
        data_zip = os.path.join(
            self.config["file_root"],
            GLOBAL.model_directory_name,
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


@before(create_temporary_dir)
@after(remove_temporary_dir)
class GetModelJSONZip:
    r"""
    Falcon service to retrieve model as zipped JSON.
    """
    def on_get(self, req, resp, unique_id):
        try:
            unarchive_model(unique_id, req.temp_dir)

            model_json = os.path.join(req.temp_dir, GLOBAL.magnetization_json_file_name)
            model_json_zip = os.path.join(req.temp_dir, GLOBAL.magnetization_json_zip_file_name)

            if not os.path.isfile(model_json):
                self.logger.debug(f"Could not find '{model_json}' in unarchived data set.")
                resp.status = falcon.HTTP_500
                return
            else:
                self.logger.debug(f"'{model_json}' found, now zipping to '{model_json_zip}' and returning")

                zout = zipfile.ZipFile(model_json_zip, "w", zipfile.ZIP_DEFLATED)
                zout.write(model_json, os.path.basename(model_json))
                zout.close()

                resp.content_type = mimetypes.guess_type(model_json_zip)[0]
                resp.stream = io.open(model_json_zip, "rb")
                resp.content_length = os.path.getsize(model_json_zip)
                return
        except ValueError as e:
            self.logger.debug(f"Could not find unique id {unique_id}")
            resp.status = falcon.HTTP_500


@before(create_temporary_dir)
@after(remove_temporary_dir)
class GetModelTecplotZip:
    r"""
    Falcon service to retrieve model as zipped tecplot.
    """
    def on_get(self, req, resp, unique_id):
        try:
            unarchive_model(unique_id, req.temp_dir)

            model_tecplot = os.path.join(req.temp_dir, GLOBAL.magnetization_tecplot_file_name)
            model_tecplot_zip = os.path.join(req.temp_dir, GLOBAL.magnetization_tecplot_zip_file_name)

            if not os.path.isfile(model_tecplot):
                self.logger.debug(f"Could not find '{model_tecplot}' in unarchived data set.")
                resp.status = falcon.HTTP_500
                return
            else:
                self.logger.debug(f"'{model_tecplot}' found, now zipping to '{model_tecplot_zip}' and returning")

                zout = zipfile.ZipFile(model_tecplot_zip, "w", zipfile.ZIP_DEFLATED)
                zout.write(model_tecplot, os.path.basename(model_tecplot))
                zout.close()

                resp.content_type = mimetypes.guess_type(model_tecplot_zip)[0]
                resp.stream = io.open(model_tecplot_zip, "rb")
                resp.content_length = os.path.getsize(model_tecplot_zip)
                return
        except ValueError as e:
            self.logger.debug(f"Could not find unique id {unique_id}")
            resp.status = falcon.HTTP_500
