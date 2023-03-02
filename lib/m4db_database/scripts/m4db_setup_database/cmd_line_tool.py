#!python
import sys
import os
import shutil
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from typer import Typer

from m4db_database.orm.schema import Base

from m4db_database import GLOBAL

from m4db_database.install.data.anisotropy_forms import populate_anisotropy_forms
from m4db_database.install.data.neb_calculation_type import populate_neb_calculation_types
from m4db_database.install.data.running_statuses import populate_running_statuses
from m4db_database.install.data.size_conventions import populate_size_conventions

app = Typer()


def setup_postgres_database(db_name, user=None, host=None, password=None, echo=False):
    r"""
    Create tables, indexes and relationships under a new database.
    Args:
        db_name: the name of the database under which to create database objects.
        user: the database user.
        host: the host on which the database lives.
        password: if a password is supplied.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.
    Returns:
        The url string to connect to the database.

    """

    if user is None and host is None and password is None:
        db_uri = GLOBAL.POSTGRES_DATABASE_URI.format(
            db_name=db_name
        )
    elif password is None:
        db_uri = GLOBAL.POSTGRES_DATABASE_USER_HOST_URI.format(
            user=user, host=host, db_name=db_name
        )
    else:
        db_uri = GLOBAL.POSTGRES_DATABASE_USER_HOST_PASSWORD_URI.format(
            user=user, host=host, db_name=db_name, password=password
        )

    if echo:
        print("Postgres uri: '{}'".format(db_uri))

    # Connect to the database
    engine = create_engine(db_uri, echo=echo, poolclass=NullPool)

    if hasattr(Base, "metadata"):
        metadata = getattr(Base, "metadata")
        metadata.create_all(engine)
    else:
        raise AssertionError("Fatal, m4db_database.orm.Base has no attribute 'metadata'")

    Session = sessionmaker(
        bind=engine,
        autoflush=True,
        autocommit=False
    )
    session = Session()

    # Add required install data.
    populate_anisotropy_forms(session)
    populate_neb_calculation_types(session)
    populate_running_statuses(session)
    populate_size_conventions(session)

    return db_uri


def mkdir_file_root(file_root):
    r"""
    Create the file root along with subdirectories.
    Args:
        file_root: the file root.

    Returns: None

    """
    pathlib.Path(file_root).mkdir(parents=True, exist_ok=True)

    # Create all the subdirectories needed.
    os.mkdir(os.path.join(file_root, GLOBAL.GEOMETRY_DIRECTORY_NAME))
    os.mkdir(os.path.join(file_root, GLOBAL.MODEL_DIRECTORY_NAME))
    os.mkdir(os.path.join(file_root, GLOBAL.NEB_DIRECTORY_NAME))


def create_file_root(file_root, yes_to_all=False):
    r"""
    Create a new file root directory to hold models, neb paths etc.
    Args:
        file_root: the file root directory which will store micromagnetic models.
        yes_to_all: if we're simply accepting all yes/no options.

    Returns:
        None.
    """
    print("Attempting to set up M4DB file_root...")

    if os.path.isdir(file_root):
        if yes_to_all:
            msg = "WARNING: '{}' already exists, delete (y/n)? y".format(file_root)
            print(msg)
            response = "y"
        else:
            msg = "WARNING: '{}' already exists, delete (y/n)? ".format(file_root)
            response = input(msg)

        if response.lower() == "y":
            shutil.rmtree(file_root)
            mkdir_file_root(file_root)
        elif response.lower() == "n":
            print("WARNING: '{}' is managed by multiple databases!".format(file_root))
        else:
            print("ERROR: unknown option!")
            sys.exit(1)
    else:
        mkdir_file_root(file_root)

    print("Done!")


def postgres(db_name, file_root, user=None, host=None, password=None, echo=False, yes_to_all=False):
    r"""
    Function to handle the postgres option.
    Args:
        db_name: database name
        file_root: the root directory of all models, neb paths, etc.
        user: database user name.
        host: url host of the database.
        password: the database password.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.
        yes_to_all: answer yes to all options.
        materials: a list of materials to add
        empty_db: do not add any data to the database.


    Returns:
        None.

    """
    create_file_root(file_root, yes_to_all=yes_to_all)

    db_uri = setup_postgres_database(db_name, user, host, password, echo)


@app.command()
def main(db_name: str, file_root: str, user: str = None, host: str = None, password: str = None, verbose: bool = False,
         yes_to_all: bool = False):
    r"""
    Create a new M4DB database.
    :param db_name: the name of the new M4DB database.
    :param file_root: the new file root - this is where models, paths etc. that are managed by M4DB are stored.
    :user: the user to which the database relations belong.
    :host: the machine host on which the database resides.
    :password: the password required to authenticate the user.
    :verbose: if this flag is set, then produce additional output as the database is created.
    :yes_to_all: if this flag is set, then 'yes' then permission is granted to all yes/no options as the database is
                 created (WARNING this means the file_root is removed!).

    """
    print(f"Attempting to create M4DB with name: '{db_name}' ...")

    postgres(
        db_name,
        file_root,
        user=user,
        host=host,
        password=password,
        echo=verbose,
        yes_to_all=yes_to_all)


def entry_point():
    app()


if __name__ == "__main__":
    app()
