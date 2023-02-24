r"""
A service to generate a scripts to run an NEB model.
"""

import json
import os

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database.orm.schema import NEB

from m4db_database import GLOBAL
from m4db_database.templates import template_env


def runner_data_with_parent(neb):
    config = read_config_from_environ()

    runner_data = {}

    # The initial path is the path belonging to the parent of this child.
    runner_data["neb_initial_path_name"] = os.path.join(
        neb.parent_neb.unique_id,
        GLOBAL.neb_tecplot_file_name
    )

    runner_data["max_energy_evaluations"] = neb.max_energy_evaluations
    runner_data["max_path_evaluations"] = neb.max_path_evaluations

    # NEB material data is taken from the start model (both start and end models should be the same).
    runner_data["materials"] = []
    for mma in neb.start_model.materials:
        runner_data["materials"].append({
            "submesh_id": mma.submesh_id,
            "name": mma.material.name,
            "temperature": mma.material.temperature,
            "ms": mma.material.ms,
            "k1": mma.material.k1,
            "aex": mma.material.aex
        })

    runner_data["external_field"] = {
        "strength": 0.0,
        "x": -1.0,
        "y": -1.0,
        "z": -1.0,
        "unit": "muT"
    }
    if neb.external_field:

        if neb.external_field.unit.symbol == "uT":
            unit_symbol = "muT"
        elif neb.external_field.unit_symbol == "mT":
            unit_symbol = "mT"
        else:
            unit_symbol = "T"

        runner_data["external_field"]["strength"] = neb.external_field.magnitude
        runner_data["external_field"]["x"] = neb.external_field.dir_x
        runner_data["external_field"]["y"] = neb.external_field.dir_y
        runner_data["external_field"]["z"] = neb.external_field.dir_z
        runner_data["external_field"]["unit"] = unit_symbol

    runner_data["energy_log_file"] = GLOBAL.energy_log_file_name

    runner_data["minimizer"] = "ConjugateGradient"
    runner_data["exchange_calculator"] = "1"

    runner_data["neb_file_name"] = GLOBAL.neb_tecplot_file_name

    return runner_data


def runner_data_without_parent(neb):
    config = read_config_from_environ()

    runner_data = {}

    # Use the geometry associated with the NEB start model (both start and end should be the same).
    runner_data["mesh_file"] = os.path.join(
        config["file_root"],
        GLOBAL.GEOMETRY_DIRECTORY_NAME,
        uid_to_dir(neb.start_model.geometry.unique_id),
        GLOBAL.GEOMETRY_PATRAN_FILE_NAME
    )

    runner_data["max_energy_evaluations"] = neb.max_energy_evaluations
    runner_data["max_path_evaluations"] = neb.max_path_evaluations

    # NEB material data is taken from the start model (both start and end models should be the same).
    runner_data["materials"] = []
    for mma in neb.start_model.materials:
        runner_data["materials"].append({
            "submesh_id": mma.submesh_id,
            "name": mma.material.name,
            "temperature": mma.material.temperature,
            "ms": mma.material.ms,
            "k1": mma.material.k1,
            "aex": mma.material.aex
        })

    # External field.
    runner_data["external_field"] = {
        "strength": 0.0,
        "x": -1.0,
        "y": -1.0,
        "z": -1.0,
        "unit": "muT"
    }
    if neb.external_field:

        if neb.external_field.unit.symbol == "uT":
            unit_symbol = "muT"
        elif neb.external_field.unit_symbol == "mT":
            unit_symbol = "mT"
        else:
            unit_symbol = "T"

        runner_data["external_field"]["strength"] = neb.external_field.magnitude
        runner_data["external_field"]["x"] = neb.external_field.dir_x
        runner_data["external_field"]["y"] = neb.external_field.dir_y
        runner_data["external_field"]["z"] = neb.external_field.dir_z
        runner_data["external_field"]["unit"] = unit_symbol

    # Start and end models.
    runner_data["start_magnetization"] = os.path.join(
        neb.start_model.unique_id,
        GLOBAL.magnetization_dat_file_name
    )
    runner_data["end_magnetization"] = os.path.join(
        neb.end_model.unique_id,
        GLOBAL.magnetization_dat_file_name
    )

    runner_data["energy_log_file"] = GLOBAL.energy_log_file_name
    runner_data["neb_path_points"] = neb.no_of_points

    runner_data["minimizer"] = "ConjugateGradient"
    runner_data["exchange_calculator"] = "1"

    runner_data["neb_file_name"] = GLOBAL.neb_tecplot_file_name

    return runner_data


class GetNEBMerrillScript:

    def on_get(self, req, resp, unique_id):
        r"""
        Get/generate a scripts to run an NEB model.
        :param req: request object.
        :param resp: response object.
        :param unique_id: the unique identifier of an NEB.
        :return: None.
        """
        config = read_config_from_environ()

        neb = self.session.query(NEB).\
            filter(NEB.unique_id == unique_id).one()

        # Depending on whether this has a parent, generate a scripts
        if neb.parent_neb:
            runner_data = runner_data_with_parent(neb)
            merrill_template = template_env("merrill").get_template("merrill_neb_child_path.jinja2")
        else:
            runner_data = runner_data_without_parent(neb)
            merrill_template = template_env("merrill").get_template("merrill_neb_root_path.jinja2")

        resp.text = json.dumps({"return": merrill_template.render(neb=runner_data)})
