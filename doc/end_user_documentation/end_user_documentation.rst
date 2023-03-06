End user documentation
======================

This end user documentation describes m4db functionality. Upon
installation, a suite of scripts with the prefix ``m4db-`` are accessible to
the user. These scripts allow someone to set up, and use the data managed by
m4db.

The m4db-user command
---------------------

The ``m4db-user`` command allows the user to add and display the users managed by m4db. It has
two subcommands ``list`` and ``add``.

The ``add`` subcommand
......................

.. program-output:: m4db-user add --help

The ``list`` subcommand
.......................

.. program-output:: m4db-user list --help

The m4db-software command
-------------------------

The ``m4db-software`` command allows the user to add and display software managed by m4db. It has
two subcommands ``list`` and ``add``.

The ``add`` subcommand
......................

.. program-output:: m4db-software add --help

The ``list`` subcommand
.......................

.. program-output:: m4db-software list --help

The ``update`` subcommand
.........................

.. program-output:: m4db-software update --help

Notes: the ``field`` option should be one of: ``name``, ``version``, ``executable``, ``description``, ``url`` or
``citation``.

The m4db-project command
------------------------

The ``m4db-project`` command allows the user to add and list the projects managed by m4db.

The ``add`` subcommand
......................

.. program-output:: m4db-project add --help

The ``list`` subcommand
.......................

.. program-output:: m4db-project list --help

The m4db-geometry command
-------------------------

The ``m4db-geometry`` command allows the user to add new geometries/meshes to m4db. These geometries will be used
as the basis of a micromagnetic local energy minimisation and will produce a model (see below). When adding a new
geometry, the user is always asked for a *size* and an *element size*, the units for both of these quantities are
**always** in **micron**. The size of a geometry can follow one of two *size conventions*: equivalent spherical
volume diameter (ESVD) or equivalent cubic volume length (ECVL).

The add-ellipsoid subcommand
............................

.. program-output:: m4db-geometry add-ellipsoid --help

Notes:

* ``size`` is in microns,
* ``element-size`` is in microns,
* ``size-convention`` should be one of ESVD or ECVL.

The add-truncated-octahedron subcommand
....................................

.. program-output:: m4db-geometry add-truncated-octahedron --help

Notes:

* ``size`` is in microns,
* ``element-size`` is in microns,
* ``size-convention`` should be one of ESVD or ECVL.

The list subcommand
...................

.. program-output:: m4db-geometry list --help

Note that ``type`` can be one of

* ``ellipsoid`` to list only ellipsoids in m4db,
* ``truncated-octahedron`` to list only truncated octahedrons in m4db.

If ``type`` is omitted, all geometries are listed.

The m4db-model command
----------------------

The ``m4db-model`` command is one of the workhorses of m4db. It's used to add a model to the database,
run the model (either directly or by scheduling the model to run via slurm) and to retrieve some information
about models from m4db. Its commands are listed as follows

The add subcommand
..................

.. program-output:: m4db-model add --help

The run subcommand
..................

.. program-output:: m4db-model run --help

The schedule subcommand
.......................

.. program-output:: m4db-model run --help

The summary subcommand
......................

.. program-output:: m4db-model summary --help
