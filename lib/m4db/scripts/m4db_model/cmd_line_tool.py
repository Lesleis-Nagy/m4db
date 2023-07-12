r"""
Perform various m4db model related actions.
"""
import os
import shutil
import sys
import json
import tempfile
import zipfile

import yaml

import schematics.exceptions
import typer
from sqlalchemy import func
from typer import Option
from typer import Argument

from subprocess import Popen, PIPE

from m4db import GLOBAL
from m4db.configuration import read_config_from_environ
from m4db.file_io.merrill_stdio import is_merrill_model_finished, read_merrill_model_stdout
from m4db.postprocessing.field_calculations import tec_to_unstructured_grid, net_quantities
from m4db.utilities.logger import setup_logger
from m4db.utilities.logger import get_logger

from m4db.orm.schema import Project, Material, Model, UniformInitialMagnetization, ModelInitialMagnetization, \
    RandomInitialMagnetization, UniformAppliedField, ModelRunData, ModelReportData, Metadata, Software, RunningStatus, \
    AnisotropyForm, RunningStatusEnum
from m4db.orm.schema import DBUser

from m4db.orm.model_creation_schema import ModelListSchema, InitialMagnetizationSchemaTypesEnum

from m4db.sessions import get_session

from m4db.db.geometry.retrieve import get_geometry

from m4db.rest_api.m4db_runner_web.get_model_run_prerequisites import get_model_run_prerequisites
from m4db.rest_api.m4db_runner_web.set_model_running_status import set_model_running_status
from m4db.rest_api.m4db_runner_web.set_model_quants import set_model_quants

from m4db.template import model_slurm_script

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
def add(model_json_file: str = Argument(..., help="a file containing new model JSON data."),
        user_name: str = Argument(..., help="the user that will own these objects."),
        project_name: str = Argument(..., help="the project that will own these objects."),
        software_name: str = Argument(..., help="the name of the software that will be used to run this model."),
        software_version: str = Argument(..., help="the version of the software that will be used to run this model."),
        dry_run: bool = Option(True, help="if this flag is set, data will be written to m4db."),
        log_file: str = Option(None, help="if supplied, logging data is saved to this file."),
        log_level: str = Option(None, help="if supplied, the level at which logging data is produced."),
        log_to_stdout: bool = Option(False, help="if set, write logging data to standard output.")):
    r"""
    Adds a new model to the database based on the input json file.
    """
    setup_logger(log_file, log_level, log_to_stdout)
    logger = get_logger()

    if not os.path.isfile(model_json_file):
        print(f"The file: '{model_json_file}' could not be found.")
        sys.exit(1)

    session = get_session()
    logger.debug("Successfully acquired session.")

    try:

        with open(model_json_file) as fin:
            models = ModelListSchema(json.load(fin))

        models.validate()
        logger.debug("Successfully validated models.")

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
                        project=existing_project,
                        software=existing_software
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
                                                      alpha=material.alpha,
                                                      theta=material.theta,
                                                      phi=material.phi,
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
        print("An unknown error occurred while attempting to write models to the database - rolling back.")
        print(e)
        session.rollback()


@app.command()
def run(unique_id: str = Argument(..., help="the unique id of the model to run."),
        log_file: str = Option(None, help="if supplied, logging data is saved to this file."),
        log_level: str = Option(None, help="if supplied, the level at which logging data is produced."),
        log_to_stdout: bool = Option(False, help="if set, write logging data to standard output.")):
    r"""
    Run a model.
    """
    setup_logger(log_file, log_level, log_to_stdout)
    logger = get_logger()
    config = read_config_from_environ()

    with tempfile.TemporaryDirectory(dir=config.database.working_root) as tmpdir:
        os.chdir(tmpdir)
        logger.debug(f"About to run a merrill script in '{os.getcwd()}'.")

        ###############################################################################################################
        # Run the model.                                                                                              #
        ###############################################################################################################

        model_run_prereqs = get_model_run_prerequisites(unique_id)

        with open(GLOBAL.MODEL_MERRILL_SCRIPT_FILE_NAME, "w") as fout:
            fout.write(f"{model_run_prereqs['merrill-script']}\n")
        logger.debug("Created model merrill script file.")

        shutil.copy(model_run_prereqs['geometry-file-abs-path'], GLOBAL.GEOMETRY_PATRAN_FILE_NAME)
        logger.debug(f"Copied geometry from {model_run_prereqs['geometry-file-abs-path']} to "
                     f"{GLOBAL.GEOMETRY_PATRAN_FILE_NAME}.")

        cmd = f"{model_run_prereqs['merrill-executable']} {GLOBAL.MODEL_MERRILL_SCRIPT_FILE_NAME}"
        logger.debug(f"Running merrill command {cmd}.")
        proc = Popen(
            cmd, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True
        )
        stdout, stderr = proc.communicate()
        logger.debug(f"Finished running command {cmd}.")

        ###############################################################################################################
        # Post-process the model.                                                                                     #
        ###############################################################################################################

        with open(GLOBAL.MODEL_STDOUT_FILE_NAME, "w") as fout:
            fout.write(f"{stdout}\n")
        logger.debug("Written standard output file.")

        with open(GLOBAL.MODEL_STDERR_FILE_NAME, "w") as fout:
            fout.write(f"{stderr}\n")
        logger.debug("Written standard error file.")

        # Check whether a file called "magnetization_mult.tec" was created - if so then rename it.
        if os.path.isfile(GLOBAL.MAGNETIZATION_MULT_TECPLOT_FILE_NAME):
            logger.debug(f"renaming "
                         f"{GLOBAL.MAGNETIZATION_MULT_TECPLOT_FILE_NAME} to "
                         f"{GLOBAL.MAGNETIZATION_TECPLOT_FILE_NAME}")
            os.rename(GLOBAL.MAGNETIZATION_MULT_TECPLOT_FILE_NAME, GLOBAL.MAGNETIZATION_TECPLOT_FILE_NAME)

        # Delete the geometry file.
        logger.debug(f"Removing geometry file {GLOBAL.GEOMETRY_PATRAN_FILE_NAME}.")
        if os.path.isfile(GLOBAL.GEOMETRY_PATRAN_FILE_NAME):
            os.remove(GLOBAL.GEOMETRY_PATRAN_FILE_NAME)
        logger.debug(f"File {GLOBAL.GEOMETRY_PATRAN_FILE_NAME} removed.")

        logger.debug(f"Magnetization output file present: {os.path.isfile(GLOBAL.MAGNETIZATION_TECPLOT_FILE_NAME)}.")
        logger.debug(f"{os.listdir()}")

        # Check output.
        logger.debug("Checking output")
        is_finished = is_merrill_model_finished(GLOBAL.MODEL_STDOUT_FILE_NAME)
        if not is_finished:
            logger.debug(f"Model unique id {unique_id} is *NOT* in finished state, setting for re-run")
            set_model_running_status(unique_id, "re-run")
            return

        with open(GLOBAL.MODEL_STDOUT_FILE_NAME) as fin:
            stdout_contents = fin.readlines()
        quants1 = read_merrill_model_stdout(stdout_contents)

        # Calculate additional quants.
        logger.debug("Calculating quants")
        ug, tec_raw = tec_to_unstructured_grid(GLOBAL.MAGNETIZATION_TECPLOT_FILE_NAME)
        quants2 = net_quantities(ug)

        # Update quants.
        set_model_quants(unique_id,
                         mx_tot=quants2["total_mx"],
                         my_tot=quants2["total_my"],
                         mz_tot=quants2["total_mz"],
                         vx_tot=quants2["total_vx"],
                         vy_tot=quants2["total_vy"],
                         vz_tot=quants2["total_vz"],
                         h_tot=quants2["total_h"],
                         rh_tot=quants2["total_rh"],
                         adm_tot=quants2["total_adm"],
                         e_typical=quants1["typical_energy_joule"],
                         e_anis=quants1["anis_energy"],
                         e_ext=quants1["ext_energy"],
                         e_demag=quants1["demag_energy"],
                         e_exch1=quants1["exch1_energy"],
                         e_exch2=quants1["exch2_energy"],
                         e_exch3=quants1["exch3_energy"],
                         e_exch4=quants1["exch4_energy"],
                         e_tot=quants1["tot_energy"])

        # Compress each file in the directory.
        logger.debug("Zipping files")
        src_files = os.listdir(".")
        src_zip_file = GLOBAL.DATA_ZIP
        zout = zipfile.ZipFile(src_zip_file, "w", zipfile.ZIP_DEFLATED)
        for src_file in src_files:
            logger.debug(f"{src_file} --> {src_zip_file}")
            zout.write(src_file)
        zout.close()

        # Copy the zipped archive to the final destination
        os.makedirs(model_run_prereqs["model-dir-abs-path"], exist_ok=True)
        shutil.copy(src_zip_file, model_run_prereqs["model-dir-abs-path"])

        # Set to finished.
        set_model_running_status(unique_id, "finished")


@app.command()
def schedule(status: str = Option(None, help="the status of the models that should be scheduled."),
             user: str = Option(None, help="the user that scheduled models belong to."),
             project: str = Option(None, help="the project that scheduled models belong to."),
             dry_run: bool = Option(True, help="a flag to indicate whether the models really should be scheduled.")):
    r"""
    Schedule a collection of models for running.
    """
    logger = get_logger()
    config = read_config_from_environ()

    with get_session() as session:

        logger.debug("Opened database session.")
        models_qry = session.query(Model)
        logger.debug("Building query.")

        if status is not None:
            logger.debug(f"The 'status' parameter is {status}, adding to query.")
            models_qry = models_qry.join(RunningStatus, Model.running_status_id == RunningStatus.id) \
                .filter(RunningStatus.name == status)
        else:
            logger.debug(f"The 'status' parameter is not supplied, only schedule 'not-run' jobs.")
            models_qry = models_qry.join(RunningStatus, Model.running_status_id == RunningStatus.id) \
                .filter(RunningStatus.name == RunningStatusEnum.not_run.value)

        if user is not None or project is not None:
            logger.debug(f"Metadata required, adding to query.")
            models_qry = models_qry.join(Metadata, Model.mdata_id == Metadata.id)
            if user is not None:
                logger.debug(f"User metadata required, adding to query.")
                models_qry = models_qry.join(DBUser, Metadata.db_user_id == DBUser.id) \
                    .filter(DBUser.user_name == user)
            if project is not None:
                logger.debug(f"Project metadata required, adding to query.")
                models_qry = models_qry.join(Project, Metadata.project_id == Project.id) \
                    .filter(Project.name == project)

        logger.debug("Retrieving models.")
        models = models_qry.all()
        logger.debug(f"Retrieved {len(models)} models.")

        if len(models) == 0:
            print("There are no models to schedule.")
        else:
            if dry_run is True:
                if len(models) == 1:
                    print(f"There is 1 model to schedule, use --no-dry-run to schedule it.")
                else:
                    print(f"There are {len(models)} models to schedule, use --no-dry-run to schedule them.")
            else:
                for model in models:
                    logger.debug(f"Scheduling model {model.unique_id}.")
                    with tempfile.NamedTemporaryFile("w") as fout:
                        fout.write(model_slurm_script(model.unique_id))
                        fout.flush()
                        logger.debug(f"Temporary slurm script written for {model.unique_id}.")

                        cmd = f"{config.scheduler.command} {fout.name}"
                        logger.debug(f"Calling scheduler with command '{cmd}'.")

                        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
                        stdout, stderr = proc.communicate()

                        logger.debug(f"stdout:\n{stdout}")
                        logger.debug(f"stderr:\n{stderr}")

                        if stderr != "":
                            print(f"An error occurred when attempting to schedule {model.unique_id}.")
                            print(stderr)
                            sys.exit(1)
                        else:
                            print(f"Scheduled {model.unique_id}.")


@app.command()
def summary():
    r"""
    Print a summary of how many models are in each system running state.
    """
    logger = get_logger()
    config = read_config_from_environ()

    with get_session() as session:
        n_not_run = session.query(func.count(Model.id)) \
            .join(RunningStatus, Model.running_status_id == RunningStatus.id) \
            .filter(RunningStatus.name == RunningStatusEnum.not_run.value) \
            .scalar()
        n_running = session.query(func.count(Model.id)) \
            .join(RunningStatus, Model.running_status_id == RunningStatus.id) \
            .filter(RunningStatus.name == RunningStatusEnum.running.value) \
            .scalar()
        n_re_run = session.query(func.count(Model.id)) \
            .join(RunningStatus, Model.running_status_id == RunningStatus.id) \
            .filter(RunningStatus.name == RunningStatusEnum.re_run.value) \
            .scalar()
        n_crashed = session.query(func.count(Model.id)) \
            .join(RunningStatus, Model.running_status_id == RunningStatus.id) \
            .filter(RunningStatus.name == RunningStatusEnum.crashed.value) \
            .scalar()
        n_finished = session.query(func.count(Model.id)) \
            .join(RunningStatus, Model.running_status_id == RunningStatus.id) \
            .filter(RunningStatus.name == RunningStatusEnum.finished.value) \
            .scalar()

        print(f"Models summary")
        print(f"Not run: {n_not_run}")
        print(f"running: {n_running}")
        print(f"re-run: {n_re_run}")
        print(f"crashed: {n_crashed}")
        print(f"finished: {n_finished}")


def entry_point():
    config = read_config_from_environ()
    setup_logger(config.logging.file, config.logging.level, config.logging.log_to_stdout)
    app()


if __name__ == "__main__":
    entry_point()
