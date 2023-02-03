import os

import yaml

from cerberus import Validator

from m4db_database.decorators import static

from m4db_database import global_vars


class Database:
    r"""
    Class to hold database information.
    """
    def __init__(self):
        self.type = None
        self.uri = None
        self.file_root = None


class Configuration:
    r"""
    Class to hold configuration information for M4DB_DATABASE.
    """
    def __init__(self):
        self.password_salt = None
        self.database = None


@static(validator=None)
def validation_schema() -> Validator:
    r"""
    Generate a cerberus validations schema to check configuration files.
    :return a cerberus validation schema"
    """
    if validation_schema.validator is None:
        validation_schema.validator = Validator()

        validation_schema.validator.schema = {
            "password-salt": {"type": "string", "required": True},
            "database": {
                "type": "dict",
                "schema": {
                    "type": {"type": "string", "regex": r"POSTGRES", "required": True},
                    "uri": {"type": "string", "required": True},
                    "file-root": {"type": "string", "required": True}
                },
                "required": True
            }
        }

    return validation_schema.validator


@static(config=None, file_name=None)
def read_config_from_file(file_name):
    r"""
    Reads an M4DB database configuration from a file, the file format must match the validation schema above.
    :param file_name the file name containing configuration information.

    """

    if read_config_from_file.config is None or read_config_from_file.file_name != file_name:
        # If the config cache is empty or the file_name associated with a config has changed, then cache a new config.
        with open(file_name, "r") as fin:
            config_dict = yaml.load(fin, Loader=yaml.FullLoader)
            if validation_schema().validate(config_dict):
                config = Configuration()
                config.database = Database()
                config.database.type = config_dict["database"]["type"]
                config.database.uri = config_dict["database"]["uri"]
                config.database.file_root = config_dict["database"]["file-root"]
                read_config_from_file.config = config
                read_config_from_file.file_name = file_name
            else:
                raise ValueError(f"Configuration file '{file_name}' is not valid.")

    return read_config_from_file.config


def read_config_from_environ():
    r"""
    Reads an M4DB database configuration by checking for an environment variable called 'M4DB_CONFIG".

    Returns:
        A python dictionary representation of M4DB database related configuration information.

    """
    file_name = os.environ.get(global_vars.M4DB_DATABASE_CONFIG_ENV_VAR)

    if file_name is None:
        raise ValueError(f"{global_vars.M4DB_DATABASE_CONFIG_ENV_VAR} environment variable doesn't exist")

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
    file_name = os.environ.get(global_vars.M4DB_DATABASE_CONFIG_ENV_VAR)

    if file_name is None:
        raise ValueError(f"{global_vars.M4DB_DATABASE_CONFIG_ENV_VAR} environment variable doesn't exist")

    return write_config_to_file(file_name, config)
