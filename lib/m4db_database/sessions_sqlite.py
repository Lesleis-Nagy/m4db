r"""
A set of utilities to create/open sqlite databases for SQLAlchemy.

@file util.sqlite.py
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
def get_session(file=None, scoped=False, echo=False, nullpool=False):
    r"""
    Retrieve an open database connection session, if file is None, then attempt to use config
    data stored in the file pointed to by the M4DB_CONFIG environment variable.

    Args:
        file: the file that will contain the database objects.
        scoped: if true return a 'scoped' session otherwise don't
        echo: boolean (default False) set to True if verbose SQLAlchemy output is required.
        nullpool: boolean (default False) we should use the null pool instead of pooled connections.

    Returns:
        A session connection to the database.
    """
    if get_session.engine is None:
        if file is None:
            config = read_config_from_environ()
            db_uri = config["db_uri"]
        else:
            db_uri = global_vars.SQLITE_FILE_URI.format(file=file)
        if nullpool:
            get_session.engine = create_engine(db_uri, echo=echo, nullpool=NullPool)
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
