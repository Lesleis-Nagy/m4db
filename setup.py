#!/usr/scripts/envs python

from setuptools import setup, find_packages

setup(
    name="m4db-db_name",
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
        "Cerberus"
    ],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    m4db-setup-database=m4db_database.scripts.m4db_setup_database:entry_point
    """
)
