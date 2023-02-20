#!/usr/scripts/envs python

from setuptools import setup, find_packages

setup(
    name="m4db-database",
    version="0.1.0",
    packages=find_packages(
        where="lib",
        include="m4db_database/*"
    ),
    package_dir={"": "lib"},
    install_requires=[
        "typer",
        "psycopg2-binary",
        "sqlalchemy",
        "pyyaml",
        "gunicorn",
        "vtk",
        "falcon",
        "gunicorn",
        "requests",
        "pandas",
        "tabulate",
        "jinja2",
        "schematics"
    ],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    m4db-setup-database=m4db_database.scripts.m4db_setup_database.cmd_line_tool:entry_point
    m4db-user=m4db_database.scripts.m4db_user.cmd_line_tool:entry_point
    m4db-software=m4db_database.scripts.m4db_software.cmd_line_tool:entry_point
    m4db-project=m4db_database.scripts.m4db_project.cmd_line_tool:entry_point
    """
)
