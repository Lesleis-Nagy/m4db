r"""
A collection of routines to add geometries to the database.
"""

import os
import shutil

from m4db_database.orm.latest import Geometry

from m4db_database.sessions import get_session

from m4db_database.utilities import uid_to_dir
from m4db_database.configuration import read_config_from_environ

from m4db_database.db.software.retrieve import retrieve_software
from m4db_database.db.software.create import create_software
from m4db_database.db.unit.retrieve import retrieve_unit
from m4db_database.db.size_convention.retrieve import retrieve_size_convention
from m4db_database.file_io.patran import read_patran
from m4db_database.utilities.geometry import geometry_volume
from m4db_database.utilities.geometry import geometry_edge_stats

from m4db_database import GLOBAL


def check_software(session, args):
    r"""
    Check to see if the required software is present in the database if it is not, then ask the user if
    a new software entry should be created.
    :param session: the database session.
    :param args: command line arguments.
    :return: a new Software object or None.
    """
    software = retrieve_software(session, args.software_name, args.software_version, allow_none=True)
    if software is None:
        # Ask for user input.
        choice = "n"
        choice = input("Software '{}' (version {}) not found, do you want to add it (y/n)?")
        if choice.lower() == "y":
            software = create_software(session,
                            args.software_name,
                            args.software_version,
                            args.software_url,
                            args.software_description,
                            args.software_citation)
        else:
            software = None

    return software


def copy_geometry_files(unique_id, patran_file, script_file, stdout_file):
    r"""
    Copy over the actual geometry file.
    :param unique_id": the unique id of the geometry.
    :param patran_file: the patran file to copy.
    :param script_file: the scripts file to copy or None.
    :param stdout_file: the stdout file to copy or None.
    :return: None.
    """
    config = read_config_from_environ()

    file_root = config["file_root"]
    dest_dir = os.path.join(
        file_root,
        GLOBAL.geometry_directory_name,
        uid_to_dir(unique_id)
    )

    # If the file root already exists we have a fatal error.
    if os.path.isdir(dest_dir):
        raise IOError(
            "The directory '{}' assosicated with unique id '{}' already exists! Please report this error to {}".format(
                dest_dir, unique_id, "l.nagy@ed.ac.uk"))
    else:
        os.makedirs(dest_dir, exist_ok=True)

    if os.path.isfile(patran_file):
        shutil.copyfile(patran_file, os.path.join(dest_dir, GLOBAL.geometry_patran_file_name))

    if script_file is not None:
        if os.path.isfile(script_file):
            shutil.copyfile(script_file, os.path.join(dest_dir, GLOBAL.geometry_script_file_name))

    if stdout_file is not None:
        if os.path.isfile(stdout_file):
            shutil.copyfile(stdout_file, os.path.join(dest_dir, GLOBAL.geometry_stdout_file_name))


def new_geometry_action(args):
    r"""
    Add a geometry to the database from data stored a dictionary.
    :param session: a database session.
    :param args: command line arguments object.
    :return: the new geometry object
    """

    session = get_session(nullpool=True)

    try:
        # Check that the patran file exists.
        if os.path.isfile(args.patran_file):
            # Process the patran file and extract data.
            patran_data = read_patran(args.patran_file)

            nelements = len(patran_data["elements"])
            nvertices = len(patran_data["vertices"])
            nsubmeshes = len(patran_data["submesh_indices"])
            mesh_volume = geometry_volume(patran_data)
            average_edge_length, stdev_edge_length, max_edge_length, min_edge_length = geometry_edge_stats(patran_data)

        else:
            raise ValueError("Patran file '{}' was not found".format(args.patran_file))

        # If the geometry scripts generation is supplied, make sure it exists.
        if args.patran_generation_script:
            has_mesh_gen_script = True
            if not os.path.isfile(args.patran_generation_script):
                raise ValueError("Patran geometry scripts '{}' supplied but not found.".format(
                    args.patran_generation_script))
        else:
            has_mesh_gen_script = False

        # If the geometry scripts generation standard output is supplied, make sure it exists.
        if args.patran_generation_stdout:
            has_mesh_gen_output = True
            if not os.path.isfile(args.patran_generation_stdout):
                raise ValueError("Patran geometry generation stdout '{}' supplied but not found.".format(
                    args.patran_generation_stdout))
        else:
            has_mesh_gen_output = False

        # Retrieve or create a new Software entry.
        software = check_software(session, args)
        if software is None:
            raise ValueError("Software details omitted.")

        # Retrieve size unit
        size_unit = retrieve_unit(session, args.geometry_size_unit)

        # Retrieve size convention
        size_convention = retrieve_size_convention(session, args.geometry_size_convention)

        geometry = Geometry(
            name=args.geometry_name,
            size=args.geometry_size,
            size_unit=size_unit,
            size_convention=size_convention,
            element_size=average_edge_length,
            element_size_unit=size_unit,
            description=args.geometry_description,
            nelements=nelements,
            nvertices=nvertices,
            nsubmeshes=nsubmeshes,
            volume_total=mesh_volume,
            has_patran=True,
            has_mesh_gen_script=has_mesh_gen_script,
            has_mesh_gen_output=has_mesh_gen_output
        )

        session.add(geometry)
        session.commit()

        # Now we copy over the files.
        copy_geometry_files(geometry.unique_id,
                            args.patran_file,
                            args.patran_generation_script,
                            args.patran_generation_stdout)

        print("Added geometry with unique ID: {}".format(geometry.unique_id))

    finally:
        session.close()