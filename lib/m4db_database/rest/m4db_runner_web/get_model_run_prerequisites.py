r"""
A service to retrieve all the data needed to run a model.
"""

import os

import falcon

import json

from m4db_database import GLOBAL

from m4db_database.configuration import read_config_from_environ

from m4db_database.orm.schema import Model

from m4db_database.template import template_loader

from m4db_database.utilities.logger import get_logger

from m4db_database.utilities.directories import geometry_directory, model_directory


class GetModelRunPrerequisites:

    def on_get(self, req, resp, unique_id):
        r"""
        Get all the prerequisites needed to run a model.

        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of a model.

        :return: None
        """
        logger = get_logger()

        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one_or_none()
        if model is None:
            resp.status = falcon.HTTP_404
            return

        logger.debug(f"Model id {unique_id}, getting merrill script.")
        merrill_template = template_loader().get_template("merrill_model.jinja2")
        merrill_script = merrill_template.render(
            model=model,
            mesh_file=GLOBAL.GEOMETRY_PATRAN_FILE_NAME,
            minimizer=GLOBAL.DEFAULT_ENERGY_MINIMIZER,
            exchange_calculator=GLOBAL.DEFAULT_EXCHANGE_CALCULATOR,
            initial_model_tecplot=GLOBAL.INITIAL_MODEL_TECPLOT_FILE_NAME,
            energy_log_file=GLOBAL.ENERGY_LOG_FILE_NAME,
            field_unit=GLOBAL.FIELD_UNIT,
            model_output=GLOBAL.MAGNETIZATION_OUTPUT_FILE_NAME)
        logger.debug(f"Model id {unique_id}, merrill script contents is complete.")

        logger.debug(f"Model id {unique_id} getting geometry path.")
        geometry_file_abs_path = os.path.join(geometry_directory(model.geometry.unique_id),
                                              GLOBAL.GEOMETRY_PATRAN_FILE_NAME)
        logger.debug(f"Model id {unique_id} geometry path is '{geometry_file_abs_path}'.")

        logger.debug(f"Model id {unique_id} getting initial destination path.")
        model_dir_abs_path = model_directory(unique_id)
        logger.debug(f"Model id {unique_id} destination path is {model_dir_abs_path}.")

        resp.text = json.dumps({
            "merrill-script": merrill_script,
            "geometry-file-abs-path": geometry_file_abs_path,
            "model-dir-abs-path": model_dir_abs_path
        })
