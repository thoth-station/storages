thoth-storages
--------------
This repo provides a library called
`thoth-storages <https://pypi.org/project/thoth-storages>`_.
The library exposes core queries and methods for JanusGraph database as well
as adapters for manipulating with Ceph via its S3 compatible API.

Installation and Usage
======================

The library can be installed via pip or pipenv:

.. code-block:: console

   pipenv install thoth-storages

The library does not provide any CLI, it is rather a low level library
supporting other parts of Thoth.

You can run prepared testsuite via the following command:

.. code-block:: console

    pipenv install --dev
    pipenv run python3 setup.py test

Automatically generate schema for Graph database
================================================

To automatically generate schema for the graph database from models defined in
this module, run:

.. code-block:: console

   # Install dev dependencies which include goblinoid:
   pipenv install --dev

   # From root of this repository:
   PYTHONPATH=. pipenv run goblinoid -m thoth.storages.graph.models -i ALL_MODELS

   # Or to directly adjust used schema:
   export PYTHONPATH=.
   # Or export also ../goblinoid to have the most recent Goblinoid version (devel from master).
   export PYTHONPATH=.:../goblinoid
   pipenv run goblinoid -m thoth.storages.graph.models -i ALL_MODELS --output-file ../janusgraph-thoth-config/scripts/init.groovy --index-file ../janusgraph-thoth-config/scripts/indexes.groovy.template

After running this command, there will be present file called `init.groovy`
which is generated automatically from models stated in `ALL_MODELS` (see file
thoth/storages/graph/models.py) as well as with indexes as configured in the
indexes.groovy.template (placed into a single file to run it in one
transaction).

See `https://github.com/thoth-station/goblinoid` for more info on how to
configure models generation.

Known Issues
============

- Gremlin queries are hanging:

   When using :code:`aiogremlin==3.3.1` (despite being not part of our specification, it might happen that another library overrides that dependency), gremlin queries might _hang indeffinitely_ without throwing any error in Jupyter Notebooks. Make sure to check that correct version of :code:`aiogremlin` is installed.
