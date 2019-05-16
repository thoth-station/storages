Thoth Storages
--------------

This library provides a library called `thoth-storages
<https://pypi.org/project/thoth-storages>`_ used in project `Thoth
<https://thoth-station.ninja>`_.  The library exposes core queries and methods
for Dgraph database as well as adapters for manipulating with Ceph via its
S3 compatible API.

Installation and Usage
======================

The library can be installed via pip or Pipenv from
`PyPI <https://pypi.org/project/thoth-storages>`_:

.. code-block:: console

   pipenv install thoth-storages

The library does not provide any CLI, it is rather a low level library
supporting other parts of Thoth.

You can run prepared testsuite via the following command:

.. code-block:: console

  pipenv install --dev
  pipenv run python3 setup.py test

  # To generate docs:
  pipenv run python3 setup.py build_sphinx

Automatically generate schema for Graph database
================================================

To automatically generate schema for the graph database from models defined in
this module, run:

.. code-block:: console

   PYTHONPATH=. pipenv run python3 ./create_schema.py --output thoth/storages/graph/schema.rdf


After running this command, the RDF file describing schema will be updated
based on changes in model.


.. code-block:: python3

  from thoth.storages import GraphDatabase

  # Also provide configuration if needed.
  graph = GraphDatabase()
  graph.connect()
  graph.initialize_schema()

