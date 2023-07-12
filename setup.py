#!/usr/scripts/envs python

from setuptools import setup, find_packages

setup(
    name="m4db",
    version="0.1.3",
    packages=find_packages(
        where="lib",
        include="m4db/*"
    ),
    package_dir={"": "lib"},
    install_requires=[
        "sphinx",
        "sphinxcontrib-programoutput",
        "docutils",
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
        "schematics",
        "pytest",
        "msgpack",
        "unittest-xml-reporting",
    ],
    include_package_data=True,
    package_data={"m4db.template": ["merrill_model.jinja2",
                                    "merrill_neb_child_path.jinja2",
                                    "merrill_neb_root_path.jinja2",
                                    "slurm_model.jinja2",
                                    "slurm_neb.jinja2"]},
    entry_points="""
    [console_scripts]
    m4db-setup-database=m4db.scripts.m4db_setup_database.cmd_line_tool:entry_point
    m4db-user=m4db.scripts.m4db_user.cmd_line_tool:entry_point
    m4db-software=m4db.scripts.m4db_software.cmd_line_tool:entry_point
    m4db-project=m4db.scripts.m4db_project.cmd_line_tool:entry_point
    m4db-geometry=m4db.scripts.m4db_geometry.cmd_line_tool:entry_point
    m4db-model=m4db.scripts.m4db_model.cmd_line_tool:entry_point
    """
)
