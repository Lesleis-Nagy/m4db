r"""
A service to generate a scripts to run a model.
"""

import json
import os

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database.orm.latest import Model
from m4db_database.orm.latest import RandomField
from m4db_database.orm.latest import UniformField
from m4db_database.orm.latest import ModelField

from m4db_database import GLOBAL
from m4db_database.templates import template_env


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
            filter(Model.unique_id == unique_id).one()

        # Runner data.

        runner_data = {}

        runner_data["mesh_file"] = os.path.join(
            config["file_root"],
            GLOBAL.geometry_directory_name,
            uid_to_dir(model.geometry.unique_id),
            GLOBAL.geometry_patran_file_name
        )

        runner_data["max_evals"] = model.max_energy_evaluations

        runner_data["minimizer"] = "ConjugateGradient"
        runner_data["exchange_calculator"] = "1"

        if isinstance(model.start_magnetization, RandomField):
            runner_data["start_magnetization"] = {
                "type": "random"
            }
        elif isinstance(model.start_magnetization, UniformField):
            runner_data["start_magnetization"] = {
                "type": "uniform",
                "x": model.start_magnetization.dir_x,
                "y": model.start_magnetization.dir_y,
                "z": model.start_magnetization.dir_z
            }
        elif isinstance(model.start_magnetization, ModelField):
            # Unpack the model
            runner_data["start_magnetization"] = {
                "type": "model",
                "tec_file": os.path.join(
                    model.start_magnetization.model.unique_id,
                    GLOBAL.magnetization_tecplot_file_name
                )
            }

        materials = []
        for mma in model.materials:
            materials.append({
                "submesh_id": mma.submesh_id,
                "name": mma.material.name,
                "temperature": mma.material.temperature,
                "ms": mma.material.ms,
                "k1": mma.material.k1,
                "aex": mma.material.aex
            })
        runner_data["materials"] = materials

        runner_data["energy_log_file"] = GLOBAL.energy_log_file_name

        runner_data["external_field"] = {
            "strength": 0.0,
            "x": -1.0,
            "y": -1.0,
            "z": -1.0,
            "unit": "muT"
        }
        if model.external_field:

            if model.external_field.unit.symbol == "uT":
                unit_symbol = "muT"
            elif model.external_field.unit_symbol == "mT":
                unit_symbol = "mT"
            else:
                unit_symbol = "T"

            runner_data["external_field"]["strength"] = model.external_field.magnitude
            runner_data["external_field"]["x"] = model.external_field.dir_x
            runner_data["external_field"]["y"] = model.external_field.dir_y
            runner_data["external_field"]["z"] = model.external_field.dir_z
            runner_data["external_field"]["unit"] = unit_symbol

        runner_data["output"] = GLOBAL.magnetization_output_file_name

        merrill_template = template_env("merrill").get_template("merrill_model.jinja2")

        resp.text = json.dumps({"return": merrill_template.render(model=runner_data)})
