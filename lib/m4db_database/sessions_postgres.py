r"""
A set of utilities to create/open postgres databases for SQLAlchemy. Note, prior to running this scripts, an empty
database should be available. This may be created with the following instructions:

    postgres=# create database <db_name> owner=<user>;

@file sessions_postgres.py
@author L. Nagy, W. Williams
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import NullPool

from m4db_database.configuration import read_config_from_environ
from m4db_database.decorators import static

from m4db_database import global_vars


@static(engine=None, Session=None)
def get_session(user=None, database=None, host=None, password=None, scoped=False, echo=False, nullpool=False):
    r"""
    Retrieve an open database connection session, if user, database and host are None then attempt to use data
    stored in M4DB_CONFIG environment variable.

    Args:
        user: the database user.
        database: the name of the database under which to create database objects.
        host: the host on which the database lives.
        password: the password to access the database with.
        scoped: if true return a 'scoped' session otherwise don't.
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.
        nullpool: boolean (default False) we should use the null pool instead of pooled connections.

    Returns:
        A session connection to the database.

    """
    if get_session.engine is None:
        if user is None and database is None and host is None:
            config = read_config_from_environ()
            db_uri = config["db_uri"]
        else:
            if user is None and host is None and password is None:
                db_uri = global_vars.POSTGRES_DATABASE_URI.format(
                    database=database
                )
            elif password is None:
                db_uri = global_vars.POSTGRES_DATABASE_USER_HOST_URI.format(
                    user=user, host=host, database=database
                )
            else:
                db_uri = global_vars.POSTGRES_DATABASE_USER_HOST_PASSWORD_URI.format(
                    user=user, host=host, database=database, password=password
                )
        if nullpool:
            get_session.engine = create_engine(db_uri, echo=echo, poolclass=NullPool)
        else:
            get_session.engine = create_engine(db_uri, echo=echo)

    if get_session.Session is None:
        get_session.Session = sessionmaker(
            bind=get_session.engine,
            autoflush=True,
            autocommit=False
        )

    if scoped:
        return scoped_session(get_session.Session)
    else:
        return get_session.Session()
