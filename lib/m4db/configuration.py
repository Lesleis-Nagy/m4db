import os

import yaml

from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types import BooleanType
from schematics.types.compound import ModelType

from m4db.decorators import static

from m4db import GLOBAL


class RunnerWeb(Model):
    r"""
    Class to hold configuration information about the runner web service.
    """
    host = StringType(regex=r"((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w\-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)",
                      required=True)
    port = IntType(required=True)
    no_of_retries = IntType(required=True, serialized_name="no-of-retries")
    backoff_factor = IntType(required=True, serialized_name="backoff-factor")


class Database(Model):
    r"""
    Class to hold configuration information about databases for M4DB_DATABASE.
    """
    type = StringType(required=True, regex=r"POSTGRES")
    uri = StringType(required=True)
    file_root = StringType(required=True, serialized_name="file-root")
    working_root = StringType(required=True, serialized_name="working-root")


class Logging(Model):
    r"""
    Class to hold logging information.
    """
    file = StringType(default=None)
    level = StringType(choices=["critical",
                                "error",
                                "warning",
                                "warn",
                                "info",
                                "debug"],
                       default="error")
    log_to_stdout = BooleanType(default=False, serialized_name="log-to-stdout")


class Configuration(Model):
    r"""
    Class to hold configuration information for M4DB_DATABASE.
    """
    password_salt = StringType(required=True, serialized_name="password-salt")
    database = ModelType(Database, required=True)
    logging = ModelType(Logging, default=Logging())
    runner_web = ModelType(RunnerWeb, required=True, serialized_name="runner-web")


def read_config_from_file(file_name: str) -> Configuration:
    r"""
    Reads an M4DB database configuration from a file, the file format must match the validation schema above.

    :param file_name the file name containing configuration information.

    :return: a configuration object.
    """
    # If the config cache is empty or the file_name associated with a config has changed, then cache a new config.
    with open(file_name, "r") as fin:
        config_dict = yaml.load(fin, Loader=yaml.FullLoader)
        config = Configuration(config_dict)
        config.validate()

    return config


@static(config=None)
def read_config_from_environ(force_reload: bool = False) -> Configuration:
    r"""
    Reads an M4DB database configuration by checking for an environment variable called 'M4DB_CONFIG".

    :param force_reload: ignore cached config info and just force the configuration information to be reloaded.

    :return: A python dictionary representation of M4DB database related configuration information.
    """
    self = read_config_from_environ
    if self.config is None or force_reload is True:
        file_name = os.environ.get(GLOBAL.M4DB_DATABASE_CONFIG_ENV_VAR)
        if file_name is None:
            raise ValueError(f"{GLOBAL.M4DB_DATABASE_CONFIG_ENV_VAR} environment variable doesn't exist")
        self.config = read_config_from_file(file_name)

    return self.config


def write_config_to_file(file_name: str, config: Configuration):
    r"""
    Writes M4DB database configuration.

    :param file_name: the file name to write configuration data to.
    :param config: a configuration object.

    :return: None.
    """
    with open(file_name, "w") as fout:
        yaml.dump(config.to_primitive(), fout, default_flow_style=False)


def write_config_to_environ(config: Configuration):
    r"""
    Writes an M4DB database configuration by checking for an environment variable called 'M4DB_CONFIG".

    :param config: the configuration data that is to be written to the environment config.

    :return: None.
    """
    file_name = os.environ.get(GLOBAL.M4DB_DATABASE_CONFIG_ENV_VAR)

    if file_name is None:
        raise ValueError(f"{GLOBAL.M4DB_DATABASE_CONFIG_ENV_VAR} environment variable doesn't exist")

    return write_config_to_file(file_name, config.to_primitive())
