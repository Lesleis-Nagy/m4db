import os

import yaml

from m4db_database.decorators import static

M4DB_CONFIG_ENTRIES = [
    "db_type", "db_uri", "file_root", "log_destination", "log_level", "log_logger_name", "mm_binary",
    "mm_binary_version", "mm_type", "authentication_salt", "m4db_runner_web", "m4db_serverside"
]

M4DB_RUNNER_WEB_ENTRIES = [
    "no_of_retries",
    "backoff_factor"
]

M4DB_SERVERSIDE_ENTRIES = [
    "default_m4db_user", "default_project", "working_dir"
]


@static(config=None)
def read_config_from_file(file_name):
    r"""
    Reads an M4DB database configuration from a file. An example configuration file looks like
        db_type: SQLITE
        db_uri: sqlite:////home/lnagy2/MMDatabase/m4db.db
        file_root: /home/lnagy2/MMDatabase/file_root
        log_destination: stdout
        log_level: DEBUG
        log_logger_name: m4db
        mm_type: MERRILL
        mm_binary: merrill
        mm_binary_version: 1.3.5
        authentication_salt: playfair
        m4db_runner_web:
            no_of_retries: 5
            backoff_factor: 1
        m4db_serverside:
            default_m4db_user: "lnagy2",
            default_project: "elongations",
            working_dir: "/var/tmp"

    Args:
        file_name: the M4DB configuration file.

    Returns:
        A python dictionary representation of M4DB database related configuration information.

    """
    if read_config_from_file.config is None:
        with open(file_name, "r") as fin:
            read_config_from_file.config = yaml.load(fin, Loader=yaml.FullLoader)
            for entry in M4DB_CONFIG_ENTRIES:
                if entry not in read_config_from_file.config.keys():
                    raise ValueError("Configuration is missing required parameter '{}'".format(entry))
            for entry in M4DB_RUNNER_WEB_ENTRIES:
                if entry not in read_config_from_file.config["m4db_runner_web"].keys():
                    raise ValueError(
                        "Configuration is missing required parameter '{}' from 'm4db_runner_web'".format(
                            entry
                        )
                    )
            for entry in M4DB_SERVERSIDE_ENTRIES:
                if entry not in read_config_from_file.config["m4db_serverside"]:
                    raise ValueError(
                        "Configuration is missing required parameter '{}' from 'm4db_serverside'".format(
                            entry
                        )
                    )
    return read_config_from_file.config


def read_config_from_environ():
    r"""
    Reads an M4DB database configuration by checking for an environment variable called 'M4DB_CONFIG".

    Returns:
        A python dictionary representation of M4DB database related configuration information.

    """
    file_name = os.environ.get("M4DB_CONFIG")

    if file_name is None:
        raise ValueError("M4DB_CONFIG environment variable doesn't exist")

    return read_config_from_file(file_name)


def write_config_to_file(file_name, config):
    r"""
    Writes M4DB database configuration.

    file_name: the file name to write configuration data to.
    config: A python dictionary representation of M4DB database related configuration information.

    Returns:
        None.

    """
    with open(file_name, "w") as fout:
        yaml.dump(config, fout, default_flow_style=False)


def write_config_to_environ(config):
    r"""
    Writes an M4DB database configuration by checking for an environment variable called 'M4DB_CONFIG".
    Args:
        config: the configuration data that is to be written to the environment config.
    Returns:
        None

    """
    file_name = os.environ.get("M4DB_CONFIG")

    if file_name is None:
        raise ValueError("M4DB_CONFIG environment variable doesn't exist")

    return write_config_to_file(file_name, config)
