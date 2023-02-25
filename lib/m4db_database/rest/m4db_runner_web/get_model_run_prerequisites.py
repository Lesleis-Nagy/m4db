r"""
A service to retrieve all the data needed to run a model.
"""

import os

import falcon

import json

from m4db_database import GLOBAL

from m4db_database.orm.schema import Model, UniformInitialMagnetization, RandomInitialMagnetization, \
    ModelInitialMagnetization, RunningStatusEnum

from m4db_database.template import template_loader
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

        model = self.session.query(Model). \
            filter(Model.unique_id == unique_id).one_or_none()
        if model is None:
            resp.status = falcon.HTTP_404
            return

        self.logger.debug(f"Model id {unique_id}, getting merrill script.")
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
        self.logger.debug(f"Model id {unique_id}, merrill script contents is complete.")

        self.logger.debug(f"Model id {unique_id} getting geometry path.")
        geometry_file_abs_path = os.path.join(geometry_directory(model.geometry.unique_id),
                                              GLOBAL.GEOMETRY_PATRAN_FILE_NAME)
        self.logger.debug(f"Model id {unique_id} geometry path is '{geometry_file_abs_path}'.")

        self.logger.debug(f"Model id {unique_id} getting initial destination path.")
        model_dir_abs_path = model_directory(unique_id)
        self.logger.debug(f"Model id {unique_id} destination path is {model_dir_abs_path}.")

        self.logger.debug(f"Model id {unique_id} getting merrill executable.")
        merrill_executable = model.mdata.software.executable
        self.logger.debug(f"Model id {unique_id} model executable is {merrill_executable}.")

        if isinstance(model.initial_magnetization, ModelInitialMagnetization):
            self.logger.debug(f"Model id {unique_id}, starts with an exiting model magnetization.")

            if model.initial_magnetization.model.running_status == RunningStatusEnum.finished:
                self.logger.debug(f"Model id {unique_id}, start magnetization is in finished state.")
                initial_magnetization_data_zip = os.path.join(
                    model_directory(model.initial_magnetization.model.unique_id),
                    GLOBAL.DATA_ZIP
                )

                if os.path.isfile(initial_magnetization_data_zip):
                    self.logger.debug(
                        f"Model id {unique_id}, start magnetization zip file {initial_magnetization_data_zip}."
                    )

                    resp.text = json.dumps({"return": {
                        "merrill-script": merrill_script,
                        "geometry-file-abs-path": geometry_file_abs_path,
                        "model-dir-abs-path": model_dir_abs_path,
                        "merrill-executable": merrill_executable,
                        "initial-magnetization-type": model.initial_magnetization.type,
                        "initial-magnetization-data-zip": initial_magnetization_data_zip,
                        "initial-magnetization-finished": True
                    }})

                    return

                else:
                    self.logger.error(
                        f"Model id {unique_id}, start magnetization zip file {initial_magnetization_data_zip} "
                        f"is missing.")

                    resp.status = falcon.HTTP_500

                    resp.body = json.dumps({
                        "error": f"Model id {unique_id}, starts with an initial magnetization from an existing model "
                                 f"(unique id: {model.initial_magnetization.model.unique_id}) with a 'finished' "
                                 f"running status, however the expected data file {initial_magnetization_data_zip} "
                                 f"does not exist on the system!"})

                    return
            else:
                self.logger.debug(f"Model id {unique_id}, start magnetization is in a non-finished state.")

                resp.text = json.dumps({"return": {
                    "merrill-script": merrill_script,
                    "geometry-file-abs-path": geometry_file_abs_path,
                    "model-dir-abs-path": model_dir_abs_path,
                    "merrill-executable": merrill_executable,
                    "initial-magnetization-type": model.initial_magnetization.type,
                    "initial-magnetization-data-zip": None,
                    "initial-magnetization-finished": False
                }})
                return
        else:
            self.logger.debug(f"Model id {unique_id}, starts with a random or uniformly magnetized state.")

            resp.text = json.dumps({"return": {
                "merrill-script": merrill_script,
                "geometry-file-abs-path": geometry_file_abs_path,
                "model-dir-abs-path": model_dir_abs_path,
                "merrill-executable": merrill_executable,
                "initial-magnetization-type": model.initial_magnetization.type,
                "initial-magnetization-data-zip": None,
                "initial-magnetization-finished": None
            }})
            return
