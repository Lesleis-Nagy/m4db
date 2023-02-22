r"""
A selection of routines to deal with archiving.
"""
import os
import zipfile

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities import uid_to_dir
from m4db_serverside import global_vars


def archive_dir(directory):
    r"""
    Archive the contents of a directory in to a file (contained within that directory).
    :param directory:
    :return:
    """

    if os.path.isdir(directory):
        # Switch to the model directory (if it exists).
        os.chdir(directory)

        # Check that the data archive is present.
        src_files = os.listdir(".")
        if global_vars.data_zip in src_files:
            return
        else:
            # If the data archive is *not* present, create it.
            with zipfile.ZipFile(global_vars.data_zip, "w", zipfile.ZIP_DEFLATED) as zout:
                for src_file in src_files:
                    zout.write(src_file)
                zout.close()


def unarchive_to_dir(archive, directory):
    r"""
    Unarchive a file to the given directory.
    :param archive: the source archive
    :param directory: the destination directory.
    :return: None
    """
    if not os.path.isfile(archive):
        raise ValueError(f"The source archive '{archive}' does not exist")
    if not os.path.isdir(directory):
        raise ValueError(f"The destination directory '{directory}' does not exist")

    with zipfile.ZipFile(archive, "r") as zout:
        zout.extractall(directory)


def archive_model(unique_id):
    r"""
    Archive a model.
    :param unique_id: the unique id of a model.
    :return: None
    """
    config = read_config_from_environ()

    model_path = os.path.join(
        config["file_root"],
        global_vars.model_directory_name,
        uid_to_dir(unique_id)
    )

    archive_dir(model_path)


def archive_neb(unique_id):
    r"""
    Archive an NEB.
    :param unique_id: the unique ID of an NEB.
    :return: None
    """
    config = read_config_from_environ()

    neb_path = os.path.join(
        config["file_root"],
        global_vars.NEB_DIRECTORY_NAME,
        uid_to_dir(unique_id)
    )

    archive_dir(neb_path)


def unarchive_model(unique_id, destination):
    r"""
    Unarchive a model.
    :param unique_id: the unique Id of a model.
    :param destination: the destination where the archive is placed.
    :return: the absolute path directory in which the model has been unarchived
    """
    config = read_config_from_environ()

    model_archive = os.path.join(
        config["file_root"],
        global_vars.model_directory_name,
        uid_to_dir(unique_id),
        global_vars.data_zip
    )

    unarchive_to_dir(model_archive, destination)


def unarchive_neb(unique_id, destination):
    r"""
    Unarchive an NEB.
    :param unique_id: the unique ID of an NEB.
    :param destination: the destination where the NEB is placed.
    :return: the absolute path directory in which the NEB has been archived.
    """
    config = read_config_from_environ()

    model_archive = os.path.join(
        config["file_root"],
        global_vars.NEB_DIRECTORY_NAME,
        uid_to_dir(unique_id),
        global_vars.data_zip
    )

    unarchive_to_dir(model_archive, destination)
