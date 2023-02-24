r"""
Global variables.
"""

import re
from datetime import datetime


class GLOBAL:
    r""""
    Dummy class to define some global variables.
    """

    # The global field unit
    FIELD_UNIT = "mT"

    # The global size unit
    SIZE_UNIT = "um"

    # Unique ids
    HEX_RE_STR = r'[0-9A-Fa-f]'
    UID_REGEX = r'{hx:}{{8}}-{hx:}{{4}}-{hx:}{{4}}-{hx:}{{4}}-{hx:}{{12}}'.format(hx=HEX_RE_STR)

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

    M4DB_DATABASE_CONFIG_ENV_VAR = "M4DB_CONFIG_FILE"

    SALTED_PASSWORD_FORMAT = "{password}{salt}"

    REGEX_SOFTWARE_AND_VERSION = re.compile(r"([a-zA-Z0-9]+)@([0-9.-]+)")

    GEOMETRY_PATRAN_FILE_NAME = "geometry.pat"
    GEOMETRY_EXODUS_FILE_NAME = "geometry.e"
    GEOMETRY_SCRIPT_FILE_NAME = "geometry.cubit"
    GEOMETRY_STDOUT_FILE_NAME = "geometry.stdout"

    # The global logger name.
    LOGGER_NAME = "m4db_database"

    # The format used for logging.
    LOGGER_FORMAT = "%(asctime)s — %(levelname)s — %(pathname)s:%(funcName)s:%(lineno)d — %(message)s"

    # The default minimizer to use.
    DEFAULT_ENERGY_MINIMIZER = "ConjugateGradient"

    # The default exchange calculator.
    DEFAULT_EXCHANGE_CALCULATOR = "1"

    # The energy log files for all runs are all named this.
    ENERGY_LOG_FILE_NAME = "energy"

    # Data is always archived as
    DATA_ZIP = "data.zip"

    # The name of a magnetization .dat file.
    MAGNETIZATION_DAT_FILE_NAME = "magnetization.dat"

    # The name of a magnetization tecplot file.
    MAGNETIZATION_TECPLOT_FILE_NAME = "magnetization.tec"

    # The name of a magnetization zip file.
    MAGNETIZATION_TECPLOT_ZIP_FILE_NAME = "magnetization.zip"

    # The name of a magnetization JSON file.
    MAGNETIZATION_JSON_FILE_NAME = "magnetization.json"

    # The name of a zipped magnetization JSON file.
    MAGNETIZATION_JSON_ZIP_FILE_NAME = "magnetization_json.zip"

    # The name of a magnetization_mult.tec file (these are produced by merrill).
    MAGNETIZATION_MULT_TECPLOT_FILE_NAME = "magnetization_mult.tec"

    # The magnetization output name used in merrill (to produce magnetization_mult.tec) files.
    MAGNETIZATION_OUTPUT_FILE_NAME = "magnetization"

    # When running models that have parent models, the parent tecplot file is copied to the working dir with this name
    INITIAL_MODEL_TECPLOT_FILE_NAME = "initial_model.tec"




    model_merrill_script_file_name = "model_script.merrill"
    model_stdout_file_name = "model_stdout.txt"
    model_stderr_file_name = "model_stderr.txt"






    neb_merrill_script_file_name = "neb_script.merrill"
    neb_stdout_file_name = "neb_stdout.txt"
    neb_stderr_file_name = "neb_stderr.txt"
    neb_mult_tecplot_file_name = "neb_mult.tec"
    neb_tecplot_file_name = "neb.tec"
    neb_path_json = "neb_path.json"

    running_status_not_run = "not-run"
    running_status_re_run = "re-run"
    running_status_running = "running"
    running_status_finished = "finished"
    running_status_crashed = "crashed"
    running_status_scheduled = "scheduled"
    running_status_failed = "failed"

    m4db_serverside_config_environment_variable = "M4DB_SERVERSIDE_CONFIG"

    default_db_user_ticket_length = 3600

    geometry_default_size_unit = "um"
    geometry_default_size_convention = "ESVD"
