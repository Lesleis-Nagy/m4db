r"""
Routines to retrieve a logger.
"""

import logging

from m4db_database.decorators import static

from m4db_database.configuration import read_config_from_environ


@static(logger=None)
def get_logger():
    config = read_config_from_environ()

    if get_logger.logger is None:
        get_logger.logger = logging.getLogger(config["log_logger_name"])

        log_level = config["log_level"]
        llevel = None
        if log_level.lower() == "debug":
            llevel = logging.DEBUG
        elif log_level.lower() == "info":
            llevel = logging.INFO
        elif log_level.lower() == "warning":
            llevel = logging.WARNING
        elif log_level.lower() == "error":
            llevel = logging.ERROR
        elif log_level.lower() == "critical":
            llevel = logging.CRITICAL
        else:
            raise ValueError(f"Unknown logging level '{log_level}'")

        log_destination = config["log_destination"]
        if log_destination == 'stdout':
            stream_handler = logging.StreamHandler()
            get_logger.logger.setLevel(llevel)
            get_logger.logger.addHandler(stream_handler)
        else:
            file_handler = logging.FileHandler(log_destination, "w")
            get_logger.logger.setLevel(llevel)
            get_logger.logger.addHandler(file_handler)

    return get_logger.logger
