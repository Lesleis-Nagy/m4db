#!/usr/scripts/envs python

from setuptools import setup, find_packages

setup(
    name="m4db-database",
    version="1.0.0a",
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
        "Cerberus",
        "vtk",
        "falcon",
        "gunicorn",
        "requests",
        "pandas",
        "tabulate",
        "jinja2",
    ],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    m4db-setup-database=m4db_database.scripts.m4db_setup_database:entry_point
    m4db-user=m4db_database.scripts.m4db_user.cmd_line_tool:entry_point
    m4db-software=m4db_database.scripts.m4db_software.cmd_line_tool:entry_point
    """
)
