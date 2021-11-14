import os
from typing import List

import yaml

from m4db_database.decorators import static

M4DB_CONFIG_ENTRIES = [
    "db_type", "db_uri", "file_root", "log_destination", "log_level", "log_logger_name",
    "authentication_salt", "m4db_runner_web", "m4db_serverside"
]

M4DB_RUNNER_WEB_ENTRIES = [
    "no_of_retries",
    "backoff_factor",
    "protocol",
    "host",
    "port"
]

M4DB_SERVERSIDE_ENTRIES = [
    "default_m4db_user",
    "default_m4db_project",
    "default_micromag_software",
    "default_micromag_software_version",
    "slurm_exe",
    "working_dir",
    "module_dir"
]


def is_list_of_str(obj):
    r"""
    Checks that obj is a list of strings
    Args:
        obj: an object

    Returns: True if 'obj' is a list of 'str', otherwise False.

    """
    return isinstance(obj, list) and all(isinstance(elem, str) for elem in obj)


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
        authentication_salt: playfair
        m4db_runner_web:
            no_of_retries: 5,
            backoff_factor: 1
            host: localhost
            port: 8081
        m4db_serverside:
            default_m4db_user: lnagy2
            default_m4db_project: elongations
            default_micromag_software: merrill
            default_micromag_software_version: 1.4.0
            slurm_exe: sbatch
            working_dir: /var/tmp
            module_dir: /dir/to/modules
            module_list:
                python/3.7.1
                m4db/1.2.0
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
            # m4db_serverside config
            for entry in M4DB_SERVERSIDE_ENTRIES:
                if entry not in read_config_from_file.config["m4db_serverside"]:
                    raise ValueError(
                        "Configuration is missing required parameter '{}' from 'm4db_serverside'".format(
                            entry
                        )
                    )
            # .. handle 'm4db_serverside' 'modules'
            if "modules" in read_config_from_file.config["m4db_serverside"].keys():
                if isinstance(read_config_from_file.config["m4db_serverside"]["modules"], str):
                    read_config_from_file.config["m4db_serverside"]["modules"] = [
                        read_config_from_file.config["m4db_serverside"]["modules"]
                    ]
                elif is_list_of_str(read_config_from_file.config["m4db_serverside"]["modules"]):
                    # Do nothing the object is fine.
                    pass
                else:
                    raise ValueError("'modules' is supplied for 'm4db_serverside' but is not str or list of strs.")
            else:
                # There are no modules so use an empty list.
                read_config_from_file.config["m4db_serverside"]["modules"] = []


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
