Introduction
============

The micromagnetic mode metadata database (m4db) is a suite of software to
manage a large collection of micromagnetic models. The m4db is split over 
several components as shown in figure :numref:`m4db_overview`. This manual 
pertains to the `m4db-database` component which manages the storage of 
micromagnetic models along with information about those models. Conceptually,
the `m4db-database` performs two main tasks: 1) it stores data and 2) it allows
you to import and export data as shown in figure
:numref:`m4db_database_functions`.

This manual is split in to two parts. First there is a description of the
user-level scripts shown in :numref:`m4db_database_functions`. The second part
of this manual is a detailed explanation of the API which is useful for
developers of `m4db-database`.
