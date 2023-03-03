API documentation
=================

This is a complete API reference of the functionality of m4db and
is a useful reference for programmers and developers of the software.

Object relational mapping
-------------------------

The m4db uses SQLAlchemy. The current ORM documented as follows

The database user object (DBUser)
.................................

The database user object refers to a user in m4db. Model LEMs, NEBs and other data managed by m4db
belongs to a user and is a useful way of grouping simulation results.

.. sqla-model:: m4db_database.orm.schema.DBUser

The Software object
...................
The software object holds information about a piece of software or software package. Micromagnetic packages
such as Merrill have an optional executable member value that should refer to an executable on the system.

.. sqla-model:: m4db_database.orm.schema.Software
