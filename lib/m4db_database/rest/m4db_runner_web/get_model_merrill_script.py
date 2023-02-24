r"""
A service to generate a scripts to run a model.
"""

import falcon
import json
import os

from m4db_database.configuration import read_config_from_environ

from m4db_database.orm.schema import Model

from m4db_database import GLOBAL
from m4db_database.template import template_loader


class GetModelMerrillScript:

    def on_get(self, req, resp, unique_id):
        r"""
        Get/generate a scripts to run a model.

        :param req: request object.
        :param resp: response object.

        :param unique_id: the unique identifier of a model.

        :return: None.
        """
        config = read_config_from_environ()

        # Retrieve associated runner data.
        model = self.session.query(Model).\
            filter(Model.unique_id == unique_id).one_or_none()

        if model is None:
            resp.status = falcon.HTTP_404

        # Runner data.

        merrill_template = template_loader().get_template("merrill_model.jinja2")

        resp.text = json.dumps({"return": merrill_template.render(
            model=model,
            mesh_file=GLOBAL.GEOMETRY_PATRAN_FILE_NAME,
            minimizer=GLOBAL.DEFAULT_ENERGY_MINIMIZER,
            exchange_calculator=GLOBAL.DEFAULT_EXCHANGE_CALCULATOR,
            initial_model_tecplot=GLOBAL.INITIAL_MODEL_TECPLOT_FILE_NAME,
            energy_log_file=GLOBAL.ENERGY_LOG_FILE_NAME,
            field_unit=GLOBAL.FIELD_UNIT,
            model_output=GLOBAL.MAGNETIZATION_OUTPUT_FILE_NAME
        )})
