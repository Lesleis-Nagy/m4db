#!/usr/scripts/envs python

from distutils.core import setup

NAME = "m4db-database"
VERSION = "1.2.0"

setup(
    name=NAME,
    version=VERSION,
    license="MIT",
    description="M4DB database core tools and utilities",
    url="https://github.com/Lesleis-Nagy/{name:}".format(name=NAME),
    download_url="https://github.com/Lesleis-Nagy/{name:}/archive/{version:}.zip".format(name=NAME, version=VERSION),
    keywords=["micromagnetics", "database"],
    install_requires=[
        "Deprecated>=1.2.13",
        "PyYAML>=5.4.1",
        "SQLAlchemy>=1.4.25",
        "falcon>=3.0.1",
        "gunicorn>=20.1.0",
        "numpy>=1.21.2",
        "pandas>=1.3.3",
        "psycopg2>=2.9.1",
        "requests>=2.26.0",
        "tqdm>=4.62.3",
        "twine>=3.4.2",
        "wheel>=0.34.2",
        "jinja2>=3.0.1",
        "vtk>=9.0.3"
    ],
    author="L. Nagy, W. Williams",
    author_email="lnagy2@ed.ac.uk",
    packages=[
        "m4db_database",
        "m4db_database.orm"
    ],
    package_dir={
        "m4db_database": "lib/m4db_database"
    },
    scripts=[
        "scripts/m4db_export_anisotropy_form",
        "scripts/m4db_export_database_from_neb",
        "scripts/m4db_export_db_user",
        "scripts/m4db_export_geometry",
        "scripts/m4db_export_material",
        "scripts/m4db_export_model",
        "scripts/m4db_export_neb",
        "scripts/m4db_export_neb_calculation_type",
        "scripts/m4db_export_physical_constant",
        "scripts/m4db_export_project",
        "scripts/m4db_export_running_status",
        "scripts/m4db_export_size_convention",
        "scripts/m4db_export_software",
        "scripts/m4db_export_unit",
        "scripts/m4db_import_anisotropy_form",
        "scripts/m4db_import_database_from_neb",
        "scripts/m4db_import_db_user",
        "scripts/m4db_import_geometry",
        "scripts/m4db_import_material",
        "scripts/m4db_import_neb_calculation_type",
        "scripts/m4db_import_physical_constant",
        "scripts/m4db_import_size_convention",
        "scripts/m4db_import_software",
        "scripts/m4db_import_unit",
        "scripts/m4db_set_micromagnetics_code",
        "scripts/m4db_setup_database"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]),
