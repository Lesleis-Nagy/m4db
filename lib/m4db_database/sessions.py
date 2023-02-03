r"""
Set of utilities to open databases.
"""

from m4db_database.configuration import read_config_from_environ

from m4db_database import global_vars

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from m4db_database.orm.latest import Base as BaseLatest
from m4db_database.orm.v1_schema import Base as BaseV1
from m4db_database.orm.v2_schema import Base as BaseV2


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

    if config.database.type == global_vars.POSTGRES_DATABASE_TYPE:
        from m4db_database.sessions_postgres import get_session
        return get_session(scoped=scoped, echo=echo, nullpool=nullpool)
    if config.database.type == global_vars.SQLITE_DATABASE_TYPE:
        from m4db_database.sessions_sqlite import get_session
        return get_session(scoped=scoped, echo=echo)

    raise ValueError(f"Unsupported database in configuration.")


def get_session_from_args(db_type, **kwargs):
    r"""
    Retrieve an SQLAlchemy open database connection session from the user's input arguments.
    :param db_type: the database type.
    :param kwargs: other keyword arguments.
    :return: a database session.
    """
    echo = kwargs["echo"] if "echo" in kwargs.keys() else False
    nullpool = kwargs["nullpool"] if "nullpool" in kwargs.keys() else False
    autoflush = kwargs["autoflush"] if "autoflush" in kwargs.keys() else False
    autocommit = kwargs["autocommit"] if "autocommit" in kwargs.keys() else False

    uri = None
    if db_type == "postgres":
        if "db_name" not in kwargs.keys():
            raise ValueError("When using 'postgres', the parameter 'db_name' is required.")

        db_name = kwargs["db_name"]
        user = kwargs["user"] if "user" in kwargs.keys() else None
        host = kwargs["host"] if "host" in kwargs.keys() else None
        password = kwargs["password"] if "password" in kwargs.keys() else None

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
    elif db_type == "sqlite":
        if "file" not in kwargs.keys():
            raise ValueError("When using 'sqlite', the parameter 'file' is mandatory")
        uri = global_vars.SQLITE_FILE_URI.format(file=kwargs["file"])

    if nullpool:
        engine = create_engine(uri, poolclass=NullPool, echo=echo)
    else:
        engine = create_engine(uri)

    if "create" in kwargs.keys():
        if kwargs["create"]:
            # Create the database.
            if "db_version" in kwargs.keys():
                if kwargs["db_version"] == "v1":
                    Base = BaseV1
                elif kwargs["db_version"] == "v2":
                    Base = BaseV2
                else:
                    Base = BaseLatest
            else:
                Base = BaseLatest

            if hasattr(Base, "metadata"):
                metadata = getattr(Base, "metadata")
                metadata.create_all(engine)
            else:
                raise AssertionError("Fatal, m4db_database.orm.Base has no attribute 'metadata'")

    Session = sessionmaker(
        bind=engine,
        autoflush=autoflush,
        autocommit=autocommit
    )

    return Session()
