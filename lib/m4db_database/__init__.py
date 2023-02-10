r"""
Global variables.
"""

import re
from datetime import datetime


class GLOBAL:
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

    REGEX_SOFTWARE_AND_VERSION = re.compile(r"([a-zA-Z0-9]+)@([0-9.-]+)")

    # Specification for the geometry name syntax:
    # Capture group 1: the geometry base name
    #               3: is the size
    #               5: is the unit
    #               6: is the size convention
    #               8: is the aspect ratio
    REGEX_TRUNCATED_CUBOCTAHEDRA = re.compile(r"^([a-z]+):(([0-9]+(\.[0-9]+)?)(m|cm|mm|um|nm|pm)):(ESVD|ECVL):(([0-9]+(\.[0-9]+)?)ar)$")















    model_directory_name = "model"
    geometry_directory_name = "geometry"
    neb_directory_name = "neb"

    geometry_patran_file_name = "geometry.pat"
    geometry_stdout_file_name = "geometry.stdout"
    geometry_script_file_name = "geometry.cubit"

    energy_log_file_name = "energy"

    data_zip = "data.zip"

    magnetization_dat_file_name = "magnetization.dat"
    magnetization_tecplot_file_name = "magnetization.tec"
    magnetization_tecplot_zip_file_name = "magnetization.zip"
    magnetization_json_file_name = "magnetization.json"
    magnetization_json_zip_file_name = "magnetization_json.zip"
    magnetization_mult_tecplot_file_name = "magnetization_mult.tec"
    magnetization_output_file_name = "magnetization"

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
