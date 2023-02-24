r"""
Perform various m4db model related actions.
"""
import os
import sys
import json
import yaml

import schematics.exceptions
import typer

import pandas as pd

from tabulate import tabulate

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.logger import setup_logger
from m4db_database.utilities.logger import get_logger

from m4db_database.orm.schema import Project, Material, Model, UniformInitialMagnetization, ModelInitialMagnetization, \
    RandomInitialMagnetization, UniformAppliedField, ModelRunData, ModelReportData, Metadata, Software, RunningStatus, \
    AnisotropyForm
from m4db_database.orm.schema import DBUser

from m4db_database.orm.model_creation_schema import ModelListSchema, InitialMagnetizationSchemaTypesEnum

from m4db_database.sessions import get_session

from m4db_database.db.geometry.retrieve import get_geometry

app = typer.Typer()


def print_validation_error_message(e):
    r"""
    Print a validation error message given an exception object.

    :param e: the exception object

    :return: None
    """
    data = e.to_primitive()
    print("Model file validation has failed, please examine the following trace ...")
    print(yaml.dump(data, default_flow_style=False))


@app.command()
def add(model_json_file: str, user_name: str, project_name: str, software_name: str, software_version: str,
        dry_run: bool = True):
    r"""
    Adds a new model to the database based on the input json file.

    :param model_json_file: a file containing new model JSON data.
    :param user_name: the user that will own these objects.
    :param project_name: the project that will own these objects.
    :param software_name: the name of the software that will be used to run this model.
    :param software_version: the version of the software that will be used to run this model.
    :param dry_run: a flag to indicate that we only wish to validate and dry-run the models given in the input JSON file
                    by default this is on (i.e. --dry-run flag is automatically set), set this flag to --no-dry-run
                    to write the data to the database.
    :return: None
    """

    if not os.path.isfile(model_json_file):
        print(f"The file: '{model_json_file}' could not be found.")
        sys.exit(1)

    session = get_session()

    try:

        with open(model_json_file) as fin:
            models = ModelListSchema(json.load(fin))

        models.validate()

        # Get user.
        existing_user = session.query(DBUser).filter(DBUser.user_name == user_name).one_or_none()
        if existing_user is None:
            print(f"The user '{user_name}' does not exist.")
            sys.exit(1)

        # Get project.
        existing_project = session.query(Project).filter(Project.name == project_name).one_or_none()
        if existing_project is None:
            print(f"The project '{project_name}' does not exist.")
            sys.exit(1)

        # Get software.
        existing_software = session.query(Software). \
            filter(Software.name == software_name). \
            filter(Software.version == software_version). \
            one_or_none()
        if existing_software is None:
            print(f"The software: '{software_name}' at version '{software_version}' could not be found.")
            sys.exit()

        # Perform additional checks.
        for index, model in enumerate(models.models):

            existing_geometry = get_geometry(session, schema_object=model.geometry)
            if existing_geometry is None:
                print(f"Could not find geometry for model in position {index}.")
                sys.exit(1)

            if model.initial_magnetization.type == InitialMagnetizationSchemaTypesEnum.model.value:
                existing_model = session.query(Model). \
                    filter(Model.unique_id == model.initial_magnetization.unique_id). \
                    one_or_none()
                if existing_model is None:
                    print(f"Could not find model for initial model magnetization with unique id: "
                          f"{model.initial_magnetization.unique_id}")
                    sys.exit(1)

            if model.unique_id is not None:
                existing_model = session.query(Model). \
                    filter(Model.unique_id == model.unique_id). \
                    one_or_none()
                if existing_model is not None:
                    print(f"Attempting to add a model with specified unique id in position {index}, however this "
                          f"id ({model.unique_id}) is already present.")
                    sys.exit(1)

            if len(model.materials) != existing_geometry.nsubmeshes:
                print(f"When attempting to add a model, the chosen geometry has {existing_geometry.nsubmeshes} "
                      f"however only {len(model.materials)} material elements were given.")
                sys.exit(1)

        # If the user is intent on putting these models in the database, then perform the action.
        if dry_run is False:
            for index, model in enumerate(models.models):

                existing_geometry = get_geometry(session, schema_object=model.geometry)

                not_run_status = session.query(RunningStatus).filter(RunningStatus.name == "not-run").one()

                for rep in range(model.reps):

                    # Create a new initial magnetization.
                    if model.initial_magnetization.type == InitialMagnetizationSchemaTypesEnum.uniform.value:
                        new_initial_magnetization = UniformInitialMagnetization(
                            dir_x=model.initial_magnetization.dir_x,
                            dir_y=model.initial_magnetization.dir_y,
                            dir_z=model.initial_magnetization.dir_z,
                            magnitude=model.initia_magnetization.magnitude
                        )
                    elif model.initial_magnetization.type == InitialMagnetizationSchemaTypesEnum.model.value:
                        existing_model = session.query(Model). \
                            filter(Model.unique_id == model.initial_magnetization.unique_id). \
                            one()
                        new_initial_magnetization = ModelInitialMagnetization(
                            model=existing_model
                        )
                    elif model.initial_magnetization.type == InitialMagnetizationSchemaTypesEnum.random.value:
                        new_initial_magnetization = RandomInitialMagnetization()
                    else:
                        print("Fatal error!")
                        sys.exit(1)

                    # Create new applied field.
                    if model.applied_field:
                        new_applied_field = UniformAppliedField(
                            dir_x=model.applied_field.dir_x,
                            dir_y=model.applied_field.dir_y,
                            dir_z=model.applied_field.dir_z,
                            magnitude=model.applied_field.magnitude
                        )
                    else:
                        new_applied_field = None

                    new_model_run_data = ModelRunData()
                    new_model_report_data = ModelReportData()
                    new_metadata = Metadata(
                        db_user=existing_user,
                        project=existing_project
                    )

                    # Create new materials.
                    new_materials = []
                    for material in model.materials:
                        existing_anisotropy_form = session.query(AnisotropyForm). \
                            filter(AnisotropyForm.name == material.anisotropy_form). \
                            one_or_none()

                        new_materials.append(Material(name=material.name,
                                                      temperature=material.temperature,
                                                      k1=material.k1, k2=material.k2, k3=material.k3,
                                                      k4=material.k4, k5=material.k5, k6=material.k6,
                                                      k7=material.k7, k8=material.k8, k9=material.k9,
                                                      k10=material.k10,
                                                      aex=material.aex,
                                                      ms=material.ms,
                                                      dir_x=material.dir_x,
                                                      dir_y=material.dir_y,
                                                      dir_z=material.dir_z,
                                                      anisotropy_form=existing_anisotropy_form,
                                                      submesh_id=material.submesh_id))

                    new_model = Model(
                        unique_id=model.unique_id if model.unique_id is not None else None,
                        max_energy_evaluations=model.max_energy_evaluations,
                        geometry=existing_geometry,
                        materials=new_materials,
                        initial_magnetization=new_initial_magnetization,
                        applied_field=new_applied_field,
                        running_status=not_run_status,
                        model_run_data=new_model_run_data,
                        model_report_data=new_model_report_data,
                        mdata=new_metadata
                    )
                    session.add(new_model)
            session.commit()
        else:
            print("Validation succeeded, if you want to add models please use the --no-dry-run flag.")

    except schematics.exceptions.ValidationError as e:
        print_validation_error_message(e)

    except schematics.exceptions.DataError as e:
        print_validation_error_message(e)

    except Exception as e:
        print("An unknown error occured while attempting to write models to the database - rolling back.")
        print(e)
        session.rollback()


@app.command()
def run(unique_id: str):
    config = read_config_from_environ()
    logger = get_logger()


def entry_point():
    config = read_config_from_environ()
    setup_logger(config.logging.file, config.logging.level, config.logging.log_to_stdout)
    app()


if __name__ == "__main__":
    entry_point()
