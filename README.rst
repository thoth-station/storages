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

Running Dgraph locally
======================

You can use `docker-compose` present in this repository to run a local Dgraph instance. It does not use TLS certificates (so you must not to provide `GRAPH_TLS_PATH` environment variable).

.. code-block:: console

  $ docker-compose up

After running the command above (make sure your big fat daemon is up using `systemctl start docker`), you should be able to access a local Dgraph instance at `localhost:9080`. This is also the default configuration for Dgraph's adapter - you don't need to provide `GRAPH_SERVICE_HOST` explicitly.

The provided `docker-compose` has also Ratel enabled for to have an UI for graph database content. To access it visit `http://localhost:8000/ <http://localhost:8080>`_.

The provided `docker-compose` uses volume mounted from `/tmp`. After you computer restart, the content will not be available anymore.
