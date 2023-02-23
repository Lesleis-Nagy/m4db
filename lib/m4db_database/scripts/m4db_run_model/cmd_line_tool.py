r"""
Run a model.
"""

import typer

from m4db_database.configuration import read_config_from_environ
from m4db_database.utilities.logger import setup_logger
from m4db_database.utilities.logger import get_logger

app = typer.Typer()


@app.command()
def run():
    logger = get_logger()
    logger.info(f"Hello!")


def entry_point():
    config = read_config_from_environ()
    setup_logger(config.logging.filename, config.logging.level, config.logging.log_to_stdout)
    app()


if __name__ == "__main__":
    entry_point()
