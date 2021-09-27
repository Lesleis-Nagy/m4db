# M4DB database

Authors: L. Nagy, W. Williams

This code contains the core database submodule for the MicroMagnetic Model Metadata DataBase (M4DB). It deals mainly with

1) creating of a new M4DB database,
2) upgrading a database from version `n` to version `n+1`,
3) importing data,
4) exporting data.

## Preprocessing/environment setup
If you are installing a development version of the M4DB, it is sometimes useful to work with Python's 
[virtual environments](https://docs.python.org/3/tutorial/venv.html). The following is not a comprehensive 
tutorial on Python virtual environments, but enough to get you started. Firstly check that you are not running
an existing virtual environment, this is usually indicated as a name in parenthesis to the of the dollar sign
at the prompt

```css
(virtual_env_name) $> 
```

You can deactivate the environment by using

```css
(virtual_env_name) $> deactivate
```

[Anaconda](https://www.anaconda.com/) sometimes adds `base` to the prompt, you can deactivate it using the `conda` command.

```css
(base) $> conda deactivate
```

To create a new virtual environment (in python 3.*)

```css
$> python -m venv <path_to_venv>/m4db_server
```

then to activate the environment execute

```css
$> source <path_to_venv>/m4db_server/bin/activate
```
Once activated you can install library packages local to that environment in the usual way:
```css
(m4db_server) $> pip install <package name>
```
To deactivate a local environment

```css
(m4db_server) $> deactivate
```

If you do use virtual environments then you might consider creating a different virtual environment for each of
the server-side and client-side install groups because they have slightly different library package requirements.

The server-side installations of [m4db_database](https://bitbucket.org/micromag/m4db_database/src/master/), 
[m4db_core](https://bitbucket.org/micromag/m4db_core/src/master/) and 
[m4db_rest_server](https://bitbucket.org/micromag/m4db_rest_server/src/master/) are ONLY required 
if you wish to have your own local version of the database.
This requires the following packages to be pip installed into your local environment:
* psycopg2 (or if not available use psycopg2-binary)
* sqlalchemy
* pyyaml
* tqdm


The **client side** installation requires fewer packages to install instructions for this are given in the README of the
Bitbucket repository [m4db_client_script](https://bitbucket.org/micromag/m4db_client_script/src/master/).

The rest of the instructions here assume installation in to a virtual environment called `m4db_server`, however
this is not necessary.

## Installation a local copy of the database

At this point we assume you have a copy of the Bitbucket repository `m4db_database` and you have navigated to
where it is located. The setup script `setup.py` may be used to install the database component of M4DB. It is installed
in the usual way

```css
(m4db_server) $> python setup.py install
```

Once installed, M4DB provides a bunch of scripts each prefixed with `m4db_`, with the name of the 
script following the underscore. To set up a new database, we can use the `m4db_setup_database` script which
will create a new database. As of writing only [SQLite](https://www.sqlite.org/index.html) and 
[Postgres](https://www.postgresql.org/) are supported. Help for the `m4db_setup_database` command can be accessed
using the `help` switch

```css
(m4db_server) $> m4db_setup_database --help
```

For development, it is easier to set up an SQLite database on a local machine. However details for setting up
Postgres and SQLite are similar

### Setting up an SQLite database
In order to set up an SQLight database issue the following command

```css
(m4db_server) $> m4db_setup_database sqlite <path_to_sqlite_file> <path_to_file_root> <path_to_config_file>
```

The `m4db_setup_database` command tells the script to create an SQLite database, with the actual database file
residing at the location `path_to_sqlite_file`. The `path_to_file_root` should be a directory that will
contain all of our models, NEB paths etc. Finally `path_to_config_file` is an absolute path to a 
file which will contain database configuration data. 

### Setting up a postgres database
In order to set up a Postgres database, there must be an existing, empty, Postgres database (referred to here as 
`database`) and a user (called `user`) that can create tables, read and write data. The following full command 
will create a Postgres M4DB database.

```css
(m4db_server) $> m4db_setup_database postgres <user> <database> <host> <path_to_file_root> <path_to_config_file> 
```

Here the `host` is the url that accesses the Postgres database. If you are running postgres on your local machine, 
then the <host> will be 127.0.0.1, and you may optionally specify the port number as part of the host address as 
127.0.0.1:5433. If you do not specify a port it will default to 5432. Make sure that postgres is using port 5432, 
or else the port number you have stated explicitly as part of the host address.\
Optionally you can authenticate with a password by using the `password`, however if you do this then the password will 
be stored in the M4DB config file as plain text!

### After database setup
Once the database is set up with the `m4db_setup_database` script, you will need set the `M4DB_CONFIG`
environment variable to point to the file location where `path_to_config_file` was written. A helpful message 
should be displayed upon successful termination of the `m4db_setup_database` utility to remind you to do this.
```css
(m4db_server) $> export M4DB_CONFIG=<full_path>/m4db.yaml
```


## Importing sample data
If you wish to import some sample data, then a small data set is available on 
[Zenodo](https://zenodo.org/record/3937446#.XxhZGhHTWAY), please make sure you're using the latest version of 
this data set! To import the data, simply unzip the data archive from Zenodo to a convenient directory (refered to as
`dir_path`) and then use the `m4db_import_database_from_neb` command

```css
(m4db_server) $> m4db_import_database_from_neb <dir_path>
```

As long as `M4DB_CONFIG` is pointing to a valid M4DB configuration file, the script should connect to the
database and begin importing data from the sample data set.

Packaging
---------
This information is useful if you plan to create an M4DB pip package. Make sure that the virtual environment
that M4DB is in is active, usually you source the environment (in this case called `m4db_server`).

```css
$> source <path_to_venvs>/m4db_server/bin/activate
```

Next you create the distribution
```css
(m4db_server) $> python setup.py sdist
```

This should create a directory called `dist` in which there will 
be a zip file called `m4db_database-<version>.linux-x86_64.tar.gz`.
Where the version is set in `setup.py`. To upload to PyPi
```css
(m4db_server) $> twine upload dist/m4db_database-<version>.tar.gz
```
this will ask for your username/password.
