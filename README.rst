Thoth Storages
--------------

.. image:: https://img.shields.io/github/v/tag/thoth-station/storages?style=plastic
  :target: https://github.com/thoth-station/storages/releases
  :alt: GitHub tag (latest by date)

.. image:: https://img.shields.io/pypi/v/thoth-storages?style=plastic
  :target: https://pypi.org/project/thoth-storages
  :alt: PyPI - Module Version

.. image:: https://img.shields.io/pypi/l/thoth-storages?style=plastic
  :target: https://pypi.org/project/thoth-storages
  :alt: PyPI - License

.. image:: https://img.shields.io/pypi/dm/thoth-storages?style=plastic
  :target: https://pypi.org/project/thoth-storages
  :alt: PyPI - Downloads

This library provides a library called `thoth-storages
<https://pypi.org/project/thoth-storages>`__ used in project `Thoth
<https://thoth-station.ninja>`__.  The library exposes core queries and methods
for `PostgreSQL database <https://www.postgresql.org/>`__ as well as adapters
for manipulating with `Ceph <https://ceph.io/>`__ via its S3 compatible API.

Quick Start
===========

Pre-requisites:

* make sure you have ``podman`` and ``podman-compose`` installed. You can install those tools by running ``dnf install -y podman podman-compose``
* make sure you are in an environment created with ``pipenv install --dev``

To develop locally the first time:

* Have a pg dump that you can `retrieve from aws s3
  <https://github.com/thoth-station/storages#automatic-backups-of-thoth-deployment>`__

* Get the latest PostgreSQL container image from: https://catalog.redhat.com/software/containers/rhel8/postgresql-13/5ffdbdef73a65398111b8362?container-tabs=gti&gti-tabs=red-hat-login

* Run ``podman-compose up`` to scale up pods for database and pgweb. For more detail, refer to the `Running PostgreSQL locally section
  <https://github.com/thoth-station/storages#running-postgresql-locally>`__

* Run this command to sync the pg dump into the local database:

  .. code-block:: console

    psql -h localhost -p 5432 --username=postgres < pg_dump.sql


Now you are ready to test new queries or `create new migrations
<https://github.com/thoth-station/storages#generating-migrations-and-schema-adjustment-in-deployment>`__

If you already have a local database, make sure it is not outdated and rember to follow the `Generating migrations and schema adjustment in deployment
<https://github.com/thoth-station/storages#generating-migrations-and-schema-adjustment-in-deployment>`__
section before testing any changes.

Installation and Usage
======================

The library can be installed via pip or Pipenv from `PyPI
<https://pypi.org/project/thoth-storages>`__:

.. code-block:: console

   pipenv install thoth-storages

The library provides a CLI that can assist you with exploring schema and data
storing:

.. code-block:: console

  thoth-storages --help
  # In a cloned repo, run:
  PYTHONPATH=. pipenv run python3 thoth-storages --help

You can run prepared test-suite via the following command:

.. code-block:: console

  pipenv install --dev
  pipenv run python3 setup.py test


Running PostgreSQL locally
==========================

You can use ``docker-compose.yaml`` present in this repository to run a local
PostgreSQL instance, (make sure you installed `podman-compose
<https://github.com/containers/podman-compose>`__):

.. code-block:: console

  $ dnf install -y podman podman-compose
  $ # Also available from PyPI: pip install podman-compose
  $ podman-compose up

After running the commands above, you should be able to access a local
PostgreSQL instance at `localhost:5432 <http://localhost:5432>`__. This is also
the default configuration for PostgreSQL's adapter that connects to localhost
unless ``KNOWLEDGE_GRAPH_HOST`` is supplied explicitly (see also other
environment variables in the adapter constructor for more info on configuring
the connection). The default configuration uses database named ``postgres``
which can be accessed using ``postgres`` user and ``postgres`` password (SSL is
disabled).

The provided ``docker-compose.yaml`` has also `PGweb
<https://sosedoff.github.io/pgweb/>`__ enabled to enable data exploration using
UI. To access it visit `localhost:8081 <http://localhost:8081>`__.

The provided ``docker-compose.yaml`` does not use any volume. After you
containers restart, the content will not be available anymore.

You can sync your local instance using ``pgsql``:

.. code-block:: console

  $ psql -h localhost -p 5432 --username=postgres < pg_dump.sql

If you would like to experiment with PostgreSQL programmatically, you can use
the following code snippet as a starting point:

.. code-block:: python

  from thoth.storages import GraphDatabase

  graph = GraphDatabase()
  graph.connect()
  # To clear database:
  # graph.drop_all()
  # To initialize schema in the graph database:
  # graph.initialize_schema()

Generating migrations and schema adjustment in deployment
=========================================================

If you make any changes to data model of the main PostgreSQL database, you need
to generate migrations. These migrations state how to adjust already existing
database with data in deployments. For this purpose, `Alembic migrations
<https://alembic.sqlalchemy.org>`__ are used. Alembic can (`partially
<https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect>`__)
automatically detect what has changed and how to adjust already existing
database in a deployment.

Alembic uses incremental version control, where each migration is versioned and
states how to migrate from previous state of database to the desired next state
- these versions are present in ``alembic/versions`` directory and are
automatically generated with procedure described bellow.

If you make any changes, follow the following steps which will generate version
for you:

* Make sure your local PostgreSQL instance is running (follow `Running
  PostgreSQL locally` instructions above):

  .. code-block:: console

    $ podman-compose up

* Run Alembic CLI to generate versions for you:

  .. code-block:: console

    # Make sure you have your environment setup:
    # pipenv install --dev
    # Make sure you are running the most recent version of schema:
    $ PYTHONPATH=. pipenv run alembic upgrade head
    # Actually generate a new version:
    $ PYTHONPATH=. pipenv run alembic revision --autogenerate -m "Added row to calculate sum of sums which will be divided by 42"

* Review migrations generated by Alembic. Note `NOT all changes are
  automatically detected by Alembic
  <https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect>`__.

* Make sure generated migrations are part of your pull request so changes are
  propagated to deployments:

  .. code-block:: console

    $ git add thoth/storages/data/alembic/versions/

* In a deployment, use Management API and its ``/graph/initialize`` endpoint to
  propagate database schema changes in deployment (Management API has to have
  recent schema changes present which are populated with new ``thoth-storages``
  releases).

* If running locally and you would like to propagate changes, run the following
  Alembic command to update migrations to the latest version:

  .. code-block:: console

    $ PYTHONPATH=. pipenv run alembic upgrade head

  If you would like to update schema programmatically run the following Python
  code:

  .. code-block:: python

    from thoth.storages import GraphDatabase

    graph = GraphDatabase()
    graph.connect()
    graph.initilize_schema()

When updating a deployment, make sure all the components use the same database
schema. Metrics exposed from a deployment should state schema version of all
the components in a deployment.

Generate schema images
======================

You can use shipped CLI ``thoth-storages`` to automatically generate schema
images out of the current models:

.. code-block:: console

  # First, make sure you have dev packages installed:
  $ pipenv install --dev
  $ PYTHONPATH=. pipenv run python3 ./thoth-storages generate-schema

The command above will produce an image named ``schema.png``. Check ``--help``
to get more info on available options.

If the command above fails with the following exception:

.. code-block:: console

  FileNotFoundError: [Errno 2] "dot" not found in path.

make sure you have ``graphviz`` package installed:

.. code-block:: console

  dnf install -y graphviz

Creating own performance indicators
===================================

Performance indicators report performance aspect of a library on `Amun
<https://github.com/thoth-station/amun-api>`__ and results can be automatically
synced if the following procedure is respected.

To create own performance
indicator, create a script which tests desired functionality of a library. An
example can be matrix multiplication script present in `thoth-station/performance
<https://github.com/thoth-station/performance/blob/master/tensorflow/matmul.py>`__
repository. This script can be supplied to `Dependency Monkey
<https://thoth-station.ninja/docs/developers/adviser/dependency_monkey.html>`__
to validate certain combination of libraries in desired runtime and buildtime
environment. Please follow instructions on how to create a performance script
shown in the `README of performance repo
<https://github.com/thoth-station/performance>`__.

To create relevant models, adjust
``thoth/storages/graph/models_performance.py`` file and add your model.
Describe parameters (reported in ``@parameters`` section of performance
indicator result) and result (reported in ``@result``). The name of class
should match ``name`` which is reported by performance indicator run.

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

All the models use `SQLAchemy <https://www.sqlalchemy.org/>`__.  See `docs
<https://docs.sqlalchemy.org/>`__ for more info.

Online debugging of queries
===========================

You can print to logger all the queries that are performed to a PostgreSQL
instance. To do so, set the following environment variable:

.. code-block:: console

  export THOTH_STORAGES_DEBUG_QUERIES=1

Memory usage statisticts
========================

You can print information about PostgreSQL adapter together with statistics on
the adapter in-memory cache usage to logger (it has to have at least level
``INFO`` set). To do so, set the following environment variable:

.. code-block:: console

  export THOTH_STORAGES_LOG_STATS=1

These statistics will be printed once the database adapter is destructed.

Automatic backups of Thoth deployment
=====================================

In each deployment, an automatic knowledge `graph backup cronjob
<https://github.com/thoth-station/graph-backup-job>`__ is run, usually once a
day. Results of automatic backups are stored on Ceph - you can find them in
``s3://<bucket-name>/<prefix>/<deployment-name>/graph-backup/pg_dump-<timestamp>.sql``.
Refer to deployment configuration for expansion of parameters in the path.

To create a database instance out of this backup file, run a fresh local
PostgreSQL instance and fill it from the backup file:

.. code-block:: console

  $ cd thoth-station/storages
  $ aws s3 --endpoint <ceph-s3-endpoint> cp s3://<bucket-name>/<prefix>/<deployment-name>/graph-backup/pg_dump-<timestamp> pg_dump-<timestamp>.sql
  $ podman-compose up
  $ psql -h localhost -p 5432 --username=postgres < pg_dump-<timestamp>.sql
  password: <type password "postgres" here>
  <logs will show up>

Manual backups of Thoth deployment
==================================

You can use ``pg_dump`` and ``psql`` utilities to create dumps and restore the
database content from dumps. This tool is pre-installed in the container image
which is running PostgreSQL so the only thing you need to do is execute
``pg_dump`` in Thoth's deployment in a PostgreSQL container to create a dump,
use ``oc cp`` to retrieve dump (or directly use ``oc exec`` and create the dump
from the cluster) and subsequently ``psql`` to restore the database content.
The prerequisite for this is to have access to the running container (edit
rights).

.. code-block:: console

  # Execute the following commands from the root of this Git repo:
  # List PostgreSQL pods running:
  $ oc get pod -l name=postgresql
  NAME                 READY     STATUS    RESTARTS   AGE
  postgresql-1-glwnr   1/1       Running   0          3d
  # Open remote shell to the running container in the PostgreSQL pod:
  $ oc rsh -t postgresql-1-glwnr bash
  # Perform dump of the database:
  (cluster-postgres) $ pg_dump > pg_dump-$(date +"%s").sql
  (cluster-postgres) $ ls pg_dump-*.sql   # Remember the current dump name
  (cluster-postgres) pg_dump-1569491024.sql
  (cluster-postgres) $ exit
  # Copy the dump to the current dir:
  $ oc cp thoth-test-core/postgresql-1-glwnr:/opt/app-root/src/pg_dump-1569491024.sql  .
  # Start local PostgreSQL instance:
  $ podman-compose up --detach
  <logs will show up>
  $ psql -h localhost -p 5432 --username=postgres < pg_dump-1569491024.sql
  password: <type password "postgres" here>
  <logs will show up>

You can ignore error messages related to an owner error like this:

.. code-block:: console

  STATEMENT:  ALTER TABLE public.python_software_stack OWNER TO thoth;
  ERROR:  role "thoth" does not exist

The PostgreSQL container uses user "postgres" by default which is different
from the one run in the cluster ("thoth"). The role assignment will simply not
be created but data will be available.

Syncing results of a workflow run in the cluster
================================================

Each workflow task in the cluster reports a JSON which states necessary
information about the task run (metadata) and actual results. These results of
workflow tasks are stored on object storage `Ceph <https://ceph.io/>`__ via S3
compatible API and later on synced via graph syncs to the knowledge graph. The
component responsible for graph syncs is `graph-sync-job
<https://github.com/thoth-station/graph-sync-job>`__ which is written generic
enough to sync any data and report metrics about synced data so you don't need
to provide such logic on each new workload registered in the system. To sync
your own results of job results (workload) done in the cluster, implement
related syncing logic in the `sync.py
<https://github.com/thoth-station/storages/blob/master/thoth/storages/sync.py>`__
and register handler in the ``HANDLERS_MAPPING`` in the same file. The mapping
maps prefix of the document id to the handler (function) which is responsible
for syncing data into the knowledge base (please mind signatures of existing
syncing functions to automatically integrate with ``sync_documents`` function
which is called from ``graph-sync-job``).

Query Naming conventions in Thoth
===================================

For query naming conventions, please read all the docs in `conventions for
query name
<https://github.com/thoth-station/storages/blob/master/docs/conventions/README.md>`__.

Accessing data on Ceph
======================
To access data on Ceph, you need to know ``aws_access_key_id`` and ``aws_secret_access_key`` credentials
of endpoint you are connecting to.

Absolute file path of data you are accessing is constructed as: ``s3://<bucket_name>/<prefix_name>/<file_path>``

There are two ways to initialize the data handler:

1. Configure environment variables

   .. list-table::
      :widths: 25 25
      :header-rows: 1

      * - Variable name
        - Content
      * - ``S3_ENDPOINT_URL``
        - Ceph Host name
      * - ``CEPH_BUCKET``
        - Ceph Bucket name
      * - ``CEPH_BUCKET_PREFIX``
        - Ceph Prefix
      * - ``CEPH_KEY_ID``
        - Ceph Key ID
      * - ``CEPH_SECRET_KEY``
        - Ceph Secret Key

   .. code-block:: python

       from thoth.storages.ceph import CephStore
       ceph = CephStore()


2. Initialize the object directly with parameters

   .. code-block:: python

       from thoth.storages.ceph import CephStore
       ceph = CephStore(
           key_id=<aws_access_key_id>,
           secret_key=<aws_secret_access_key>,
           prefix=<prefix_name>,
           host=<endpoint_url>,
           bucket=<bucket_name>)

After initialization, you are ready to retrieve data

.. code-block:: python

    ceph.connect()

    try:
        # For dictionary stored as json
        json_data = ceph.retrieve_document(<file_path>)

        # For general blob
        blob = ceph.retrieve_blob(<file_path>)

    except NotFoundError:
        # File does not exist


Accessing Thoth Data on the Operate-First Public Bucket
=======================================================

A public instance of Thoth's database is available on the `Operate-First Public Bucket
<https://github.com/operate-first/apps/blob/master/docs/content/odh/trino/access_public_bucket.md>`__ for external contributors to start developing components of Thoth.

Instructions for accessing the bucket are available in the `documentation
<https://github.com/thoth-station/datasets#accessing-thoth-data-on-the-operate-first-public-bucket>`__ of the `thoth/datasets
<https://github.com/thoth-station/datasets>`__ repository.

Be careful not to store any confidential or valuable information in this bucket as its content can be wiped out at any time.
