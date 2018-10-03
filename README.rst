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
    pipenv run python3 -m pytest tests/ -v
