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


Known Issues
============

- Gremlin queries are hanging:

   When using :code:`aiogremlin==3.3.1` (despite being not part of our specification, it might happen that another library overrides that dependency), gremlin queries might _hang indeffinitely_ without throwing any error in Jupyter Notebooks. Make sure to check that correct version of :code:`aiogremlin` is installed.
