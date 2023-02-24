r"""
Scripts to run a micromagnetic NEB.
"""

import os
import shutil
import tempfile
import random
import time
import zipfile
import json
import uuid

from subprocess import Popen, PIPE


from m4db_database.utilities_logging import get_logger
from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.unique_id import uid_to_dir

from m4db_database.rest_api.m4db_runner_web.is_neb_parent_blocking import is_neb_parent_blocking
from m4db_database.rest_api.m4db_runner_web.get_neb_merrill_script import get_neb_merrill_script
from m4db_database.rest_api.m4db_runner_web.get_neb_software_executable import get_neb_software_executable
from m4db_database.rest_api.m4db_runner_web.set_neb_running_status import set_neb_running_status
from m4db_database.rest_api.m4db_runner_web.get_neb_start_end_unique_ids import get_neb_start_end_unique_ids
from m4db_database.rest_api.m4db_runner_web.get_neb_parent_unique_id import get_neb_parent_unique_id

from m4db_database.file_io.merrill_stdio import extract_path_type
from m4db_database.file_io.merrill_stdio import extract_path_data
from m4db_database.file_io.merrill_stdio import count_path_fails_and_minimized

from m4db_database.utilities.archive import unarchive_model
from m4db_database.utilities.archive import unarchive_neb

from m4db_database import GLOBAL


def run_neb(unique_id):
    config = read_config_from_environ()
    logger = get_logger()

    # Wait a random amount of time based on unique_id.
    random.seed(unique_id)
    wait_time = random.randint(1, 20)
    print(f"waiting for {wait_time}")
    time.sleep(wait_time)
    print(f"activating ...")

    # Check to see whether this NEB is blocked.
    if is_neb_parent_blocking(unique_id):
        logger.debug(f"The NEB {unique_id} was blocked")
        # The parent is blocking, so we set the status and exit
        set_neb_running_status(unique_id, "not-run")
        return

    # Final destination of the NEB data.
    database_dir = os.path.join(
        config["file_root"],
        GLOBAL.NEB_DIRECTORY_NAME,
        uid_to_dir(unique_id)
    )
    logger.debug(f"NEB destination: '{database_dir}'")

    # Set the working directory root.
    working_directory = config["m4db_serverside"]["working_dir"]

    # Create the temporary directory within the working directory.

    # These lines are useful for testing
    #tmpdir = os.path.join(working_directory, str(uuid.uuid4()))
    #os.makedirs(tmpdir, exist_ok=True)
    #if os.path.isdir(tmpdir):

    with tempfile.TemporaryDirectory(dir=working_directory) as tmpdir:
        logger.debug(f"temporary working directory: '{tmpdir}'")

        # Change to the temporary working directory
        os.chdir(tmpdir)

        # Get the executable.
        executable = get_neb_software_executable(unique_id)
        logger.debug(f"Merrill executable {executable}")

        # Unarchive the start/end models.
        neb_parent_uid = get_neb_parent_unique_id(unique_id)
        start_uid = None
        end_uid = None
        if neb_parent_uid is None:
            # If the model has no parent, unpack the start/end models
            start_uid, end_uid = get_neb_start_end_unique_ids(unique_id)
            os.makedirs(start_uid)
            os.makedirs(end_uid)
            unarchive_model(start_uid, start_uid)
            unarchive_model(end_uid, end_uid)
        else:
            # If the model has a parent, then unpack that instead.
            os.makedirs(neb_parent_uid)
            unarchive_neb(neb_parent_uid, neb_parent_uid)

        # Create a MERRILL script.
        get_neb_merrill_script(unique_id, GLOBAL.neb_merrill_script_file_name)

        # Set running status to 'running'
        set_neb_running_status(unique_id, "running")

        # Execute the MERRILL script.
        logger.debug(f"executing {executable}")
        merrill_t0 = time.time()
        cmd = "{exe:} {merrill_script:}".format(
            exe=executable, merrill_script=GLOBAL.neb_merrill_script_file_name)
        proc = Popen(
            cmd,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            text=True,
            shell=True
        )
        stdout, stderr = proc.communicate()
        merrill_t1 = time.time()
        time_taken = merrill_t1 - merrill_t0
        logger.debug(f"merrill completed after {time_taken}s")

        # Remove unpacked data
        if neb_parent_uid is None:
            # If the model has no parent, unpack the start/end models
            shutil.rmtree(start_uid)
            shutil.rmtree(end_uid)
        else:
            # If the model has a parent, then unpack that instead.
            shutil.rmtree(neb_parent_uid)

        # Check whether a file called was created, if so rename it.
        if os.path.isfile(GLOBAL.neb_mult_tecplot_file_name):
            os.rename(GLOBAL.neb_mult_tecplot_file_name, GLOBAL.neb_tecplot_file_name)

        # Write standard output and standard error to files.
        with open(GLOBAL.neb_stdout_file_name, "w") as fout:
            fout.write(stdout)
        with open(GLOBAL.neb_stderr_file_name, "w") as fout:
            fout.write(stderr)

        # Check output.
        path_type = extract_path_type(GLOBAL.neb_stdout_file_name)
        if path_type == "INITIAL_PATH":
            # Do nothing.
            pass
        elif path_type == "NEB_PATH":
            n_fails, n_mins = count_path_fails_and_minimized(GLOBAL.neb_stdout_file_name)
            if n_fails > 0:
                set_neb_running_status(unique_id, "re-run")
        else:
            raise ValueError("Path is UNKNOWN_PATH")

        # Write path energies to a JSON file.
        logger.debug("Creating path energies.")
        path_energies = extract_path_data(GLOBAL.neb_stdout_file_name)
        with open(GLOBAL.neb_path_json, "w") as fout:
            fout.write(json.dumps(path_energies))

        # Compress each file in the directory.
        logger.debug("Zipping files")
        src_files = os.listdir(".")
        src_zip_file = GLOBAL.DATA_ZIP
        zout = zipfile.ZipFile(src_zip_file, "w", zipfile.ZIP_DEFLATED)
        for src_file in src_files:
            logger.debug(f"{src_file} --> {src_zip_file}")
            zout.write(src_file)
        zout.close()

        # Copy the zipped archive to the final destination.
        os.makedirs(database_dir, exist_ok=True)
        shutil.copy(src_zip_file, database_dir)

        # src_files = os.listdir(".")
        # for file_name in src_files:
        #     if os.path.isfile(file_name):
        #         logger.debug(f"Copying over file {file_name}")
        #         shutil.copy(file_name, database_dir)

        # Set status to finished.
        set_neb_running_status(unique_id, "finished")
