r"""
A collection of routines to add geometries to the database.
"""

import os
import sys
import shutil

from enum import Enum
from decimal import Decimal

import typer
from typer import Option
from typer import Argument

import pandas as pd

from tabulate import tabulate

from sqlalchemy.exc import IntegrityError

from m4db.orm.schema import Ellipsoid, Geometry
from m4db.orm.schema import TruncatedOctahedron
from m4db.orm.schema import SizeConvention
from m4db.orm.schema import SizeConventionEnum

from m4db.orm.schema import new_unique_id

from m4db.sessions import get_session
from m4db.utilities.directories import geometry_directory

from m4db.file_io.patran import read_patran
from m4db.utilities.geometry import geometry_volume
from m4db.utilities.geometry import geometry_edge_stats

from m4db.utilities.simple_formats import is_str_decimal

from m4db import GLOBAL

app = typer.Typer()

TYPE = "Type"
SIZE = "S."
ELEMENT_SIZE = "E.S."
SIZE_CONVENTION = "S.C."
NELEMENTS = "N.E."
NVERTICES = "N.V."
NSUBMESHES = "N.S."
COMPUTED_VOLUME = "V."
COMPUTED_ELEMENT_LENGTH_AVG = "E.L. avg"
COMPUTED_ELEMENT_LENGTH_STD_DEV = "E.L. s.d."
COMPUTED_ELEMENT_LENGTH_MIN = "E.L. min"
COMPUTED_ELEMENT_LENGTH_MAX = "E.L. max"
HAS_PATRAN = "Patran"
HAS_EXODUS = "Exodus"
HAS_MESH_GEN_SCRIPT = "Gen. script"
HAS_MESH_GEN_OUTPUT = "Gen. output"
PROLATENESS = "Pro."
OBLATENESS = "Obl."
ASPECT_RATIO = "A.R."
TRUNCATION_FACTOR = "T.F."


class GeometryOrAllEnum(Enum):
    r"""
    In addition to the geometries defiend in GeometryEnum add an 'all' option.
    """
    ellipsoid = "ellipsoid"
    truncated_octahedron = "truncated-octahedron"


def all_ellipsoids(session):
    r"""
    Retrieve all ellipsoids and return a Pandas DataFrame object.

    :param session: the database session.

    :return: Pandas DataFrame object containing ellipsoid data.
    """
    df_dict = {TYPE: [],
               SIZE: [],
               ELEMENT_SIZE: [],
               SIZE_CONVENTION: [],
               NELEMENTS: [],
               NVERTICES: [],
               NSUBMESHES: [],
               COMPUTED_VOLUME: [],
               COMPUTED_ELEMENT_LENGTH_AVG: [],
               COMPUTED_ELEMENT_LENGTH_STD_DEV: [],
               COMPUTED_ELEMENT_LENGTH_MIN: [],
               COMPUTED_ELEMENT_LENGTH_MAX: [],
               HAS_PATRAN: [],
               HAS_EXODUS: [],
               HAS_MESH_GEN_SCRIPT: [],
               HAS_MESH_GEN_OUTPUT: [],
               OBLATENESS: [],
               PROLATENESS: []}

    ellipsoids = session.query(Ellipsoid).all()

    if len(ellipsoids) > 0:
        for ellipsoid in ellipsoids:
            df_dict[TYPE].append(ellipsoid.type)
            df_dict[SIZE].append(ellipsoid.size)
            df_dict[ELEMENT_SIZE].append(ellipsoid.element_size)
            df_dict[SIZE_CONVENTION].append(ellipsoid.size_convention.symbol)
            df_dict[OBLATENESS].append(ellipsoid.oblateness)
            df_dict[PROLATENESS].append(ellipsoid.prolateness)
            df_dict[NELEMENTS].append(ellipsoid.nelements)
            df_dict[NVERTICES].append(ellipsoid.nvertices)
            df_dict[NSUBMESHES].append(ellipsoid.nsubmeshes)
            df_dict[COMPUTED_VOLUME].append(ellipsoid.computed_volume)
            df_dict[COMPUTED_ELEMENT_LENGTH_AVG].append(ellipsoid.computed_element_length_average)
            df_dict[COMPUTED_ELEMENT_LENGTH_STD_DEV].append(ellipsoid.computed_element_length_standard_deviation)
            df_dict[COMPUTED_ELEMENT_LENGTH_MIN].append(ellipsoid.computed_element_length_minimum)
            df_dict[COMPUTED_ELEMENT_LENGTH_MAX].append(ellipsoid.computed_element_length_maximum)
            df_dict[HAS_PATRAN].append(ellipsoid.has_patran)
            df_dict[HAS_EXODUS].append(ellipsoid.has_exodus)
            df_dict[HAS_MESH_GEN_SCRIPT].append(ellipsoid.has_mesh_gen_script)
            df_dict[HAS_MESH_GEN_OUTPUT].append(ellipsoid.has_mesh_gen_output)

    return pd.DataFrame(df_dict)


def all_truncated_octahedra(session):
    r"""
    Retrieve all truncated octahedra as a Pandas DataFrame object.

    :param session: the database session.

    :return: Pandas DataFrame object containing truncated octahedra data.
    """
    df_dict = {TYPE: [],
               SIZE: [],
               ELEMENT_SIZE: [],
               SIZE_CONVENTION: [],
               TRUNCATION_FACTOR: [],
               ASPECT_RATIO: [],
               NELEMENTS: [],
               NVERTICES: [],
               NSUBMESHES: [],
               COMPUTED_VOLUME: [],
               COMPUTED_ELEMENT_LENGTH_AVG: [],
               COMPUTED_ELEMENT_LENGTH_STD_DEV: [],
               COMPUTED_ELEMENT_LENGTH_MIN: [],
               COMPUTED_ELEMENT_LENGTH_MAX: [],
               HAS_PATRAN: [],
               HAS_EXODUS: [],
               HAS_MESH_GEN_SCRIPT: [],
               HAS_MESH_GEN_OUTPUT: []}

    truncated_octahedra = session.query(TruncatedOctahedron).all()

    if len(truncated_octahedra) > 0:
        for truncated_octahedron in truncated_octahedra:
            df_dict[TYPE].append(truncated_octahedron.type)
            df_dict[SIZE].append(truncated_octahedron.size)
            df_dict[ELEMENT_SIZE].append(truncated_octahedron.element_size)
            df_dict[SIZE_CONVENTION].append(truncated_octahedron.size_convention.symbol)
            df_dict[TRUNCATION_FACTOR].append(truncated_octahedron.truncation_factor)
            df_dict[ASPECT_RATIO].append(truncated_octahedron.aspect_ratio)
            df_dict[NELEMENTS].append(truncated_octahedron.nelements)
            df_dict[NVERTICES].append(truncated_octahedron.nvertices)
            df_dict[NSUBMESHES].append(truncated_octahedron.nsubmeshes)
            df_dict[COMPUTED_VOLUME].append(truncated_octahedron.computed_volume)
            df_dict[COMPUTED_ELEMENT_LENGTH_AVG].append(truncated_octahedron.computed_element_length_average)
            df_dict[COMPUTED_ELEMENT_LENGTH_STD_DEV].append(
                truncated_octahedron.computed_element_length_standard_deviation)
            df_dict[COMPUTED_ELEMENT_LENGTH_MIN].append(truncated_octahedron.computed_element_length_minimum)
            df_dict[COMPUTED_ELEMENT_LENGTH_MAX].append(truncated_octahedron.computed_element_length_maximum)
            df_dict[HAS_PATRAN].append(truncated_octahedron.has_patran)
            df_dict[HAS_EXODUS].append(truncated_octahedron.has_exodus)
            df_dict[HAS_MESH_GEN_SCRIPT].append(truncated_octahedron.has_mesh_gen_script)
            df_dict[HAS_MESH_GEN_OUTPUT].append(truncated_octahedron.has_mesh_gen_output)

    return pd.DataFrame(df_dict)


def copy_geometry_files(unique_id: str, patran_file: str, exodus_file: str, script_file: str, stdout_file: str,
                        create_destination: bool = False):
    r"""
    Utility function to create a destination directory in the data store and copy over each file.

    :param unique_id: the unique id of the geometry.
    :param patran_file: the patran file to copy.
    :param exodus_file: the exodus file to copy.
    :param script_file: the scripts file to copy or None.
    :param stdout_file: the stdout file to copy or None.
    :param create_destination: flag to indicate that the destination should be created (an error is raised if the
                               destination is already contains the directory).

    :return: The directory in to which geometry files were placed.
    """
    dest_dir = geometry_directory(unique_id)

    # If the file root already exists we have a fatal error.
    if os.path.isdir(dest_dir) and create_destination:
        raise IOError(f"The directory '{dest_dir}' associated with unique id '{unique_id}' already exists!")
    else:
        os.makedirs(dest_dir, exist_ok=True)

    if os.path.isfile(patran_file):
        shutil.copyfile(patran_file, os.path.join(dest_dir, GLOBAL.GEOMETRY_PATRAN_FILE_NAME))
    else:
        raise IOError(f"Could not find '{patran_file}'.")

    if exodus_file is not None:
        if os.path.isfile(exodus_file):
            shutil.copyfile(exodus_file, os.path.join(dest_dir, GLOBAL.GEOMETRY_EXODUS_FILE_NAME))
        else:
            raise IOError(f"Could not find '{exodus_file}'.")

    if script_file is not None:
        if os.path.isfile(script_file):
            shutil.copyfile(script_file, os.path.join(dest_dir, GLOBAL.GEOMETRY_SCRIPT_FILE_NAME))
        else:
            raise IOError(f"Could not find '{script_file}'.")

    if stdout_file is not None:
        if os.path.isfile(stdout_file):
            shutil.copyfile(stdout_file, os.path.join(dest_dir, GLOBAL.GEOMETRY_STDOUT_FILE_NAME))
        else:
            raise IOError(f"Could not find '{stdout_file}'.")

    return dest_dir


def save_new_geometry(session, geometry, patran_file, exodus_file, mesh_gen_script, mesh_gen_stdout):
    r"""
    Save the new geometry to the database.

    :param session: the database session.
    :param geometry: the geometry object to save.
    :param patran_file: the patran file path.
    :param exodus_file: the exodus file path.
    :param mesh_gen_script: the mesh generation script file path.
    :param mesh_gen_stdout: the mesh generation routine standard output file path.

    :return: None.
    """

    try:
        session.add(geometry)
        copy_geometry_files(geometry.unique_id, patran_file, exodus_file, mesh_gen_script, mesh_gen_stdout)

    except IntegrityError as e:
        print("Could not add geometry - possible duplicate.")
        session.rollback()

    except Exception as e:
        print("Some unknown error occurred - the geometry was not added.")
        print(e)
        session.rollback()

    finally:
        dest_dir = geometry_directory(geometry.unique_id)
        if not os.path.isdir(dest_dir):
            print("The destination files/directory was not created - rolling back database!")
            session.rollback()
        else:
            session.commit()


@app.command()
def list(type: GeometryOrAllEnum = Option(None, help="the type of geometry to list."),
         csv_file: str = Option(None, help="if specified, save the output to this csv file instead.")):
    r"""
    List the geometries in the system.
    """
    session = get_session()

    dfs = []
    if type == GeometryOrAllEnum.ellipsoid:
        df_ellipsoids = all_ellipsoids(session)
        if not df_ellipsoids.empty:
            dfs.append(df_ellipsoids)

    elif type == GeometryOrAllEnum.truncated_octahedron:
        df_truncated_octahedra = all_truncated_octahedra(session)
        if not df_truncated_octahedra.empty:
            dfs.append(df_truncated_octahedra)

    elif type is None:
        df_ellipsoids = all_ellipsoids(session)
        if not df_ellipsoids.empty:
            dfs.append(df_ellipsoids)
        df_truncated_octahedra = all_truncated_octahedra(session)
        if not df_truncated_octahedra.empty:
            dfs.append(df_truncated_octahedra)

    if len(dfs) > 1:
        df = pd.concat(dfs, axis=0, ignore_index=True)
    elif len(dfs) == 1:
        df = dfs[0]
    else:
        print("There were not results in the database.")
        sys.exit()

    if csv_file:
        df.to_csv(csv_file, index=False)
    else:
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@app.command()
def add_ellipsoid(
    patran_file: str = Argument(..., help="the geometry patran file."),
    size: str = Argument(..., help="the geometry size (in micron)."),
    element_size: str = Argument(..., help="the mesh size (in micron)."),
    size_convention: SizeConventionEnum = Argument(..., help="the size convention of the 'size' parameter."),
    prolateness: str = Argument(..., help="the prolateness of the geometry (x-length / y-length)."),
    oblateness: str = Argument(..., help="the oblateness of the geometry (y-length / z-length)."),
    exodus_file: str = Option(None, help="the geometry exodusII file."),
    mesh_gen_script: str = Option(None, help="the geometry mesh generation script."),
    mesh_gen_stdout: str = Option(None, help="the geometry standard output file.") ,
    unique_id: str = Option(None, help="if supplied, try to use this as the unique_id of the new geometry.")):
    r"""
    Create a new ellipsoid geometry.
    """
    if not (is_str_decimal(size)):
        print("Size parameter has incorrect number format.")
        sys.exit(1)
    if not (is_str_decimal(element_size)):
        print("Element size parameter has incorrect number format.")
        sys.exit(1)
    if not (is_str_decimal(oblateness)):
        print("Oblateness parameter has incorrect number format.")
        sys.exit(1)
    if not (is_str_decimal(prolateness)):
        print("Prolateness parameter has incorrect number format.")
        sys.exit(1)

    session = get_session(nullpool=True)

    if unique_id is not None:
        existing_geometry = session.query(Geometry).filter(Geometry.unique_id == unique_id).one_or_none()
        if existing_geometry is None:
            the_unique_id = unique_id
        else:
            print(f"A geometry with the unique id '{unique_id}' already exists.")
            sys.exit(1)
    else:
        the_unique_id = new_unique_id()

    vertices, elements, submesh_ids = read_patran(patran_file)

    volume = geometry_volume(vertices, elements)
    avg_edge_length, std_dev_edge_length, max_edge_length, min_edge_length = geometry_edge_stats(vertices, elements)

    has_exodus = True if exodus_file is not None and os.path.isfile(exodus_file) else False
    has_mesh_gen_script = True if mesh_gen_script is not None and os.path.isfile(mesh_gen_script) else False
    has_mesh_gen_stdout = True if mesh_gen_stdout is not None and os.path.isfile(mesh_gen_stdout) else False

    db_size_convention = session.query(SizeConvention).filter(SizeConvention.symbol == size_convention.value).one()

    geometry = Ellipsoid(
        unique_id=the_unique_id,
        nelements=len(elements),
        nvertices=len(vertices),
        nsubmeshes=len(submesh_ids),
        computed_volume=volume,
        computed_element_length_average=avg_edge_length,
        computed_element_length_standard_deviation=std_dev_edge_length,
        computed_element_length_minimum=min_edge_length,
        computed_element_length_maximum=max_edge_length,
        has_patran=True,
        has_exodus=has_exodus,
        has_mesh_gen_script=has_mesh_gen_script,
        has_mesh_gen_output=has_mesh_gen_stdout,
        size=Decimal(size),
        element_size=Decimal(element_size),
        size_convention=db_size_convention,
        prolateness=Decimal(prolateness),
        oblateness=Decimal(oblateness)
    )

    save_new_geometry(session, geometry, patran_file, exodus_file, mesh_gen_script, mesh_gen_stdout)


@app.command()
def add_truncated_octahedron(
        patran_file: str = Argument(..., help="the geometry patran file."),
        size: str = Argument(..., help="the geometry size (in micron)."),
        element_size: str = Argument(..., help="the mesh size (in micron)."),
        size_convention: SizeConventionEnum = Argument(..., help="the size convention of the 'size' parameter."),
        aspect_ratio: str = Argument(..., help="the aspect ratio of the geometry."),
        truncation_factor: str = Argument(..., help="truncation factor."),
        exodus_file: str = Option(None, help="the geometry exodusII file."),
        mesh_gen_script: str = Option(None, help="the geometry mesh generation script."),
        mesh_gen_stdout: str = Option(None, help="the geometry standard output file.") ,
        unique_id: str = Option(None, help="if supplied, try to use this as the unique_id of the new geometry.")):
    r"""
    Create a new truncated octahedron geometry.
    """
    if not (is_str_decimal(size)):
        print("Size parameter has incorrect number format.")
        sys.exit(1)
    if not (is_str_decimal(element_size)):
        print("Element size parameter has incorrect number format.")
        sys.exit(1)
    if not (is_str_decimal(aspect_ratio)):
        print("Aspect ratio parameter has incorrect number format.")
        sys.exit(1)
    if not (is_str_decimal(truncation_factor)):
        print("Truncation factor parameter has incorrect number format.")
        sys.exit(1)

    session = get_session(nullpool=True)

    if unique_id is not None:
        existing_geometry = session.query(Geometry).filter(Geometry.unique_id == unique_id).one_or_none()
        if existing_geometry is None:
            the_unique_id = unique_id
        else:
            print(f"A geometry with the unique id '{unique_id}' already exists.")
            sys.exit(1)
    else:
        the_unique_id = new_unique_id()

    vertices, elements, submesh_ids = read_patran(patran_file)

    volume = geometry_volume(vertices, elements)
    avg_edge_length, std_dev_edge_length, max_edge_length, min_edge_length = geometry_edge_stats(vertices, elements)

    has_exodus = True if exodus_file is not None and os.path.isfile(exodus_file) else False
    has_mesh_gen_script = True if mesh_gen_script is not None and os.path.isfile(mesh_gen_script) else False
    has_mesh_gen_stdout = True if mesh_gen_stdout is not None and os.path.isfile(mesh_gen_stdout) else False

    db_size_convention = session.query(SizeConvention).filter(SizeConvention.symbol == size_convention.value).one()

    geometry = TruncatedOctahedron(
        unique_id=the_unique_id,
        nelements=len(elements),
        nvertices=len(vertices),
        nsubmeshes=len(submesh_ids),
        computed_volume=volume,
        computed_element_length_average=avg_edge_length,
        computed_element_length_standard_deviation=std_dev_edge_length,
        computed_element_length_minimum=min_edge_length,
        computed_element_length_maximum=max_edge_length,
        has_patran=True,
        has_exodus=has_exodus,
        has_mesh_gen_script=has_mesh_gen_script,
        has_mesh_gen_output=has_mesh_gen_stdout,
        size=Decimal(size),
        element_size=Decimal(element_size),
        size_convention=db_size_convention,
        truncation_factor=Decimal(truncation_factor),
        aspect_ratio=Decimal(aspect_ratio)
    )

    save_new_geometry(session, geometry, patran_file, exodus_file, mesh_gen_script, mesh_gen_stdout)


def entry_point():
    app()


if __name__ == "__main__":
    app()
