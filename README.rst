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

If you would like to experiment with Dgraph programatically, you can use the following code snippet as a starting point:

.. code-block:: python

  from thoth.storages import GraphDatabase
  
  graph = GraphDatabase()
  graph.connect()
  # To clear database:
  # graph.drop_all()
  # To initialize schema in the graph database:
  # graph.initialize_schema()

Schema adjustment in deployment
===============================

It's possible to perform adjustments of schema in a deployemnt. It's important
that there are no open transactions (simply retry schema creation until it
succeeds). You can use relevant endpoint on Management API for this purpose.

If there are changes in types, Dgraph tries to automatically perform conversion
from an old type to the new one as described in the new schema (e.g. a float to
string). Invalid schema changes (e.g. parsing string into a float, but the
string cannot be parsed as a float) result in schema change errors. These errors
need to be handled programatically by deployment administrator (ideally avoid
such conversions).

Creating own performance indicators
===================================

You can create your own performance indicators. To create own performance
indicator, create a script which tests desired functionality of a library. An
example can be matrix multiplication script present in `performance
<https://github.com/thoth-station/performance/blob/master/tensorflow/matmul.py>`_
repository. This script can be supplied to Dependency Monkey to validate
certain combination of libraries in desired runtime and buildtime environment
or directly on Amun API which will run the given script using desired software
and hardware configuration. Please follow instructions on how to create a
performance script shown in the `README of performance repo
<https://github.com/thoth-station/performance>`_.

To create relevant models, adjust `thoth/storages/graph/performance.py` file
and add your model. Describe parameters (reported in `@parameters` section of
performance indicator result) and result (reported in `@result`). The name of
class should match `name` which is reported by performance indicator run.

.. code-block:: python

  @attr.s(slots=True)
  class PiMatmul(PerformanceIndicatorBase):
      """A class for representing a matrix multiplication micro-performance test."""

      SCHEMA_PARAMETERS = Schema({
          Required("matrix_size"): int,
          Required("dtype"): str,
          Required("reps"): int,
          Required("device"): str,
      })

      SCHEMA_RESULT = Schema({
          Required("elapsed"): float,
          Required("rate"): float,
      })

      # Device used during performance indicator run - CPU/GPU/TPU/...
      device = model_property(type=str, index="exact")
      matrix_size = model_property(type=int, index="int")
      dtype = model_property(type=str, index="exact")
      reps = model_property(type=int, index="int")
      elapsed = model_property(type=float)
      rate = model_property(type=float)


After you have created relevant model, register your model to `ALL_PERFORMANCE_MODELS` and re-generate graph database schema (as discussed above).

Online debugging of queries done to Dgraph
==========================================

You can print to logger all the queries that are performed to a Dgraph instance. To do so, set the following environment variables:

.. code-block::

  export THOTH_LOG_STORAGES=DEBUG
  export THOTH_STORAGES_DEBUG_QUERIES=1

