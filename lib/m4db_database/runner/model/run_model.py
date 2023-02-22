r"""
Scripts to run a micromagnetic model.
"""

import os
import shutil
import tempfile
import random
import time
import zipfile
import uuid

import simplejson as json
import numpy as np

from subprocess import Popen, PIPE

from m4db_database.utilities_logging import get_logger
from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database.rest_api.m4db_runner_web.get_model_merrill_script import get_model_merrill_script
from m4db_database.rest_api.m4db_runner_web.get_model_software_executable import get_model_software_executable
from m4db_database.rest_api.m4db_runner_web.get_model_start_magnetization import get_model_start_magnetization
from m4db_database.rest_api.m4db_runner_web.set_model_running_status import set_model_running_status
from m4db_database.rest_api.m4db_runner_web.set_model_quants import set_model_quants


from m4db_database.file_io.merrill_stdio import is_merrill_model_finished
from m4db_database.file_io.merrill_stdio import read_merrill_model_stdout

from m4db_database.postprocessing.field_calculations import tec_to_unstructured_grid
from m4db_database.postprocessing.field_calculations import net_quantities

from m4db_database.utilities.archive import unarchive_model

from m4db_database import GLOBAL


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def run_model(unique_id):
    config = read_config_from_environ()
    logger = get_logger()

    # Wait a random amount of time based on unique_id.
    random.seed(unique_id)
    wait_time = random.randint(1, 20)
    logger.info(f"waiting for {wait_time}s")
    time.sleep(wait_time)
    logger.info("activating ...")

    # This is the final destination of model data.
    database_dir = os.path.join(
        config["file_root"],
        GLOBAL.MODEL_DIRECTORY_NAME,
        uid_to_dir(unique_id)
    )
    logger.debug(f"model destination: '{database_dir}")

    # Retrieve the model's start magnetization data
    start_magnetization = get_model_start_magnetization(unique_id)
    logger.debug(f"model start magnetization info: {start_magnetization}")

    # This is the working directory.
    working_dir = config["m4db_serverside"]["working_dir"]

    # These lines are useful for testing
    #tmpdir = os.path.join(working_dir, str(uuid.uuid4()))
    #logger.debug(f"working directory: '{tmpdir}'")
    #os.makedirs(tmpdir, exist_ok=True)
    #if os.path.isdir(tmpdir):

    with tempfile.TemporaryDirectory(dir=working_dir) as tmpdir:
        logger.debug(f"working directory: '{tmpdir}'")

        # Switch to the working directory.
        os.chdir(tmpdir)

        # If this model's start magnetization is an existing model, then ...
        start_magnetization_type = start_magnetization["type"]
        if start_magnetization_type == "model":
            # retrieve the start magnetization unique ID
            start_magnetization_unique_id = start_magnetization["unique_id"]
            # retrieve the start magnetization running status
            start_magnetization_running_status = start_magnetization["running_status"]

            # If this model's start magnetization is in a finished state, then ...
            if start_magnetization_running_status == "finished":
                # ... unarchive the model
                start_magnetization_unique_id = start_magnetization["unique_id"]
                logger.debug(f"model {unique_id} requires model {start_magnetization_unique_id} ... unarchiving")
                os.makedirs(start_magnetization_unique_id, exist_ok=True)
                unarchive_model(start_magnetization_unique_id, start_magnetization_unique_id)
            else:
                # ... otherwise write to debug log and end.
                logger.debug(
                    f"model {unique_id} requires model {start_magnetization_unique_id} "
                    f"but its running status is {start_magnetization_running_status}")
                return

        # Get the executable.
        executable = get_model_software_executable(unique_id)

        # Create a Merrill script.
        get_model_merrill_script(unique_id, GLOBAL.model_merrill_script_file_name)

        # Set the running status to 'running'
        set_model_running_status(unique_id, "running")

        # Execute the merrill scripts.
        logger.debug(f"executing {executable}")
        merrill_t0 = time.time()
        cmd = "{exe:} {merrill_script:}".format(
                exe=executable, merrill_script=GLOBAL.model_merrill_script_file_name
        )
        proc = Popen(
            cmd,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            text=True,
            shell=True
        )
        stdout, stderr = proc.communicate()

        # Remove start model data if it was present
        if start_magnetization_type == "model":
            start_magnetization_unique_id = start_magnetization["unique_id"]
            logger.debug(f"removing start model directory {start_magnetization_unique_id}")
            shutil.rmtree(start_magnetization_unique_id)

        # Write standard output and standard error to files.
        logger.debug("Writing merrill standard output and standard error files.")
        with open(GLOBAL.model_stdout_file_name, "w") as fout:
            fout.write(stdout)
        with open(GLOBAL.model_stderr_file_name, "w") as fout:
            fout.write(stderr)

        merrill_t1 = time.time()
        time_taken = merrill_t1 - merrill_t0
        logger.info(f"merrill completed after {time_taken}s")

        # Check whether a file called "magnetization_mult.tec" was created - if so then rename it.
        if os.path.isfile(GLOBAL.magnetization_mult_tecplot_file_name):
            logger.debug(fr"renaming {GLOBAL.magnetization_mult_tecplot_file_name} to {GLOBAL.magnetization_tecplot_file_name}")
            os.rename(GLOBAL.magnetization_mult_tecplot_file_name, GLOBAL.magnetization_tecplot_file_name)

        # Check output.
        logger.debug("Checking output")
        is_finished = is_merrill_model_finished(GLOBAL.model_stdout_file_name)
        if not is_finished:
            logger.debug(f"Model unique id {unique_id} is *NOT* in finished state, setting for re-run")
            set_model_running_status(unique_id, "re-run")
            return

        with open(GLOBAL.model_stdout_file_name) as fin:
            stdout_contents = fin.readlines()
        quants1 = read_merrill_model_stdout(stdout_contents)

        # Calculate additional quants.
        logger.debug("Calculating quants")
        ug, tec_raw = tec_to_unstructured_grid(GLOBAL.magnetization_tecplot_file_name)
        quants2 = net_quantities(ug)

        # Save a JSON version of our model.
        logger.debug("Creating quant file")
        with open(GLOBAL.magnetization_json_file_name, "w") as fout:
            fout.write(json.dumps(tec_raw, cls=NumpyEncoder))

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
                         e_tot=quants1["tot_energy"],
                         volume=quants2["total_vol"])

        # Compress each file in the directory.
        logger.debug("Zipping files")
        src_files = os.listdir(".")
        src_zip_file = GLOBAL.data_zip
        zout = zipfile.ZipFile(src_zip_file, "w", zipfile.ZIP_DEFLATED)
        for src_file in src_files:
            logger.debug(f"{src_file} --> {src_zip_file}")
            zout.write(src_file)
        zout.close()

        # Copy the zipped archive to the final destination
        os.makedirs(database_dir, exist_ok=True)
        shutil.copy(src_zip_file, database_dir)

        # src_files = os.listdir(".")
        # for file_name in src_files:
        #     if os.path.isfile(file_name):
        #         logger.debug(f"Copying over file {file_name}")
        #         shutil.copy(file_name, database_dir)

        # Set to finished.
        set_model_running_status(unique_id, "finished")
