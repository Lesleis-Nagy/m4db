r"""
Global variables.
"""

from datetime import datetime


class global_vars:
    r""""
    Dummy class to define some global variables.
    """

    # Postgres related global variables.
    POSTGRES_DATABASE_USER_HOST_URI = "postgresql+psycopg2://{user:}@{host:}/{db_name:}"
    POSTGRES_DATABASE_HOST_URI = "postgresql+psycopg2://{host:}/{db_name:}"
    POSTGRES_DATABASE_USER_HOST_PASSWORD_URI = "postgresql+psycopg2://{user:}:{password:}@{host:}/{db_name:}"
    POSTGRES_DATABASE_URI = "postgresql+psycopg2:///{db_name:}"

    POSTGRES_DATABASE_TYPE = "POSTGRES"

    # SQLITE related global variables.
    SQLITE_FILE_URI = "sqlite:///{file:}"
    SQLITE_DATABASE_TYPE = "SQLITE"

    # Date time format
    DATE_TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"

    # Access levels
    ACCESS_ALL = 0
    ACCESS_READ = 1
    ACCESS_WRITE = 2
    ACCESS_ADMIN = 4

    # The Unix epoch start
    UNIX_EPOCH = datetime(1970, 1, 1, 0, 0, 0, 0)

    # Progress bar offset
    TQDM_POSITION = 0
    BAR_MESSAGE_FORMAT = "{:30s}"

    MODEL_DIRECTORY_NAME = "model"
    GEOMETRY_DIRECTORY_NAME = "geometry"
    NEB_DIRECTORY_NAME = "neb"

    M4DB_DATABASE_CONFIG_ENV_VAR = "M4DB_DATABASE_CONFIG"

    SALTED_PASSWORD_FORMAT = "{password}{salt}"