r"""
Set of utilities to open databases.
"""

from m4db_database.configuration import read_config_from_environ

from m4db_database import global_vars

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text


def get_session(scoped=False, echo=False, nullpool=False):
    r"""
    Retrieve an SQLAlchemy open database connection session from the M4DB_CONFIG file.
    Parameters:
        scoped: if true we return a scoped session.
        echo: if true we return a session with echoing enabled.
        nullpool: if true we return a non-pooled session.
    Returns:
        A session connection.
    """
    config = read_config_from_environ()

    if config["db_type"] == global_vars.POSTGRES_DATABASE_TYPE:
        from m4db_database.sessions_postgres import get_session
        return get_session(scoped=scoped, echo=echo, nullpool=nullpool)
    if config["db_type"] == global_vars.SQLITE_DATABASE_TYPE:
        from m4db_database.sessions_sqlite import get_session
        return get_session(scoped=scoped, echo=echo)

    raise ValueError("Unsupported db_type in M4DB_CONFIG db_type: {}".format(config["db_type"]))


def get_session_from_args(db_name, db_type, **kwargs):
    r"""
    Retrieve an SQLAlchemy open database connection session from the user's input arguments.
    :param db_name: the database db_name.
    :param db_type: the database type.
    :param kwargs: other keyword arguments.
    :return: a database session.
    """
    echo = kwargs["echo"] if "echo" in kwargs.keys() else False
    nullpool = kwargs["nullpool"] if "nullpool" in kwargs.keys() else False
    autoflush = kwargs["autoflush"] if "autoflush" in kwargs.keys() else False
    autocommit = kwargs["autocommit"] if "autocommit" in kwargs.keys() else False
    user = kwargs["user"] if "user" in kwargs.keys() else None
    host = kwargs["host"] if "host" in kwargs.keys() else None
    password = kwargs["password"] if "password" in kwargs.keys() else None

    uri = None
    if db_type == "postgres":
        if user is not None and host is not None and password is not None:
            uri = global_vars.POSTGRES_DATABASE_USER_HOST_PASSWORD_URI.format(
                database=db_name, user=user, host=host, password=password
            )
        elif user is not None and host is not None and password is None:
            uri = global_vars.POSTGRES_DATABASE_USER_HOST_URI.format(
                database=db_name, user=user, host=host
            )
        elif user is not None and host is None and password is None:
            uri = global_vars.POSTGRES_DATABASE_HOST_URI.format(
                database=db_name, user=user
            )
        elif user is None and host is None and password is None:
            uri = global_vars.POSTGRES_DATABASE_URI.format(database=db_name)
        else:
            raise ValueError("Unknown combination of parameters to connect to database.")

    if nullpool:
        engine = create_engine(uri, poolclass=NullPool)
    else:
        engine = create_engine(uri)

    Session = sessionmaker(
        bind=engine,
        autoflush=autoflush,
        autocommit=autocommit
    )

    return Session()
