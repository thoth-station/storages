Thoth Storages
--------------

This library provides a library called `thoth-storages
<https://pypi.org/project/thoth-storages>`_ used in project `Thoth
<https://thoth-station.ninja>`_.  The library exposes core queries and methods
for PostgreSQL database as well as adapters for manipulating with Ceph via its
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

Running PostgreSQL locally
==========================

You can use `docker-compose` present in this repository to run a local PostgreSQL instance:

.. code-block:: console

  $ docker-compose up

After running the command above (make sure your big fat daemon is up using `systemctl start docker`), you should be able to access a local PostgreSQL instance at `localhost:5432`. This is also the default configuration for PostgreSQL's adapter - you don't need to provide `GRAPH_SERVICE_HOST` explicitly. The default configuration uses database named `thoth` which can be accessed using `postgres` user and `postgres` password (SSL is disabled).

The provided `docker-compose` has also PGweb enabled for to have an UI for the database content. To access it visit `http://localhost:8081/ <http://localhost:8081>`_.

The provided `docker-compose` does not use any volume. After you containers restart, the content will not be available anymore.

If you would like to experiment with PostgreSQL programatically, you can use the following code snippet as a starting point:

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

TBD.

Generate schema images
======================

You can use shipped CLI ``thoth-storages`` to automatically generate schema images out of the current models:

.. code-block:: console

  # First, make sure you have dev packages installed:
  pipenv install --dev
  PYTHONPATH=. pipenv run python3 ./thoth-storages generate-schema

The command above will produce 2 images named ``schema.png`` and
``schema_cache.png``. The first PNG file shows schema for the main PostgreSQL
instance and the latter one, as the name suggests, shows how cache schema looks
like.

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

To create relevant models, adjust `thoth/storages/graph/models_performance.py` file
and add your model. Describe parameters (reported in `@parameters` section of
performance indicator result) and result (reported in `@result`). The name of
class should match `name` which is reported by performance indicator run.

.. code-block:: python

  class PiMatmul(Base, BaseExtension, PerformanceIndicatorBase):
      """A class for representing a matrix multiplication micro-performance test."""

      # Device used during performance indicator run - CPU/GPU/TPU/...
      device = Column(String(128), nullable=False)
      matrix_size = Column(Integer, nullable=False)
      dtype = Column(String(128), nullable=False)
      reps = Column(Integer, nullable=False)
      elapsed = Column(Float, nullable=False)
      rate = Column(Float, nullable=False)

All the models use `SQLAchemy <https://www.sqlalchemy.org/>`_.
See `docs <https://docs.sqlalchemy.org/>`_ for more info.

Online debugging of queries
===========================

You can print to logger all the queries that are performed to a PostgreSQL instance. To do so, set the following environment variable:

.. code-block::

  export THOTH_STORAGES_DEBUG_QUERIES=1

Online debugging of queries
===========================

You can print information about PostgreSQL adapter together with statisics on
the graph cache and memory cache usage to logger (it has to have at least level
`INFO` set). To do so, set the following environment variable:

.. code-block::

  export THOTH_STORAGES_LOG_STATS=1

These statistics will be printed once the database adapter is destructed.

Graph database cache
====================

The implementation of this library also provides a cache to speed up queries to
graph database. This cache is especially suitable for prod systems not to query
for popular packages multiple times.

The cache can be created with shipped CLI tool:

.. code-block:: console

  # When using version from this Git repository:
  PYTHONPATH=. THOTH_STORAGES_GRAPH_CACHE="cache.sqlite3" pipenv run ./thoth-storages graph-cache -c ../adviser/cache_conf.yaml

  # When using a version installed from PyPI:
  THOTH_STORAGES_GRAPH_CACHE="cache.sqlite3" thoth-storages graph-cache -c ../adviser/cache_conf.yaml

The command above creates a SQLite3 database which carries some of the data
loaded from the PostgreSQL database which help resolver resolve software stacks
faster.  The path to cache can be supplied using environment variable
``THOTH_STORAGES_GRAPH_CACHE``. By default, the module will create an in-memory
SQLite3 database and will not persist it onto disk. If the configuration points
to non-existing file, an SQLite3 database will be created and persisted onto
disk with data which were added into it based on runtime usage. This naturally
re-uses graph cache multiple times across runs (filled with the data needed) as
expected.

Take a look at adviser repo, at ``cache_conf.yaml`` file specifically, to
see how ``cache_conf.yaml`` file should be structured. An example could be:

.. code-block:: yaml

  python-packages:
   - thoth-storages
   - tensorflow

With the configuration above, the cache will be created. This cache will hold a
serialized dependency graph of TensorFlow and thoth-storages packages, together
with node information to effectively construct TensorFlow's dependency graph
for transitive queries.

Note only information which should not change over time are captured in the
cache; for example, packages which were not yet resolved during cache creation
are not added to cache so system explicitly asks for resolution results next
time (they might be resolved meanwhile).

To enable inserts into graph cache, set
``THOTH_STORAGES_GRAPH_CACHE_INSERTS_DISABLED`` to ``0`` (the default value of
``1`` disables it). Disabling inserts might be benefitial in deployments where
you want to avoid building cache (overhead needed to insert data into graph
cache, checks of uniqueness of entries and cache index creation which in sum
are expensive operations).

To disable graph cache completely, set ``THOTH_STORAGES_GRAPH_CACHE_DISABLED``
environment variable to ``1`` (the default value of ``0`` enables it).
