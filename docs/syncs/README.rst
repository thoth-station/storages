Thoth Storages syncs into Thoth Databse
----------------------------------------

Thoth collects several type of observations and sync them using `graph-sync-job <https://github.com/thoth-station/graph-sync-job>`_
To make sure that everything is consistent, we use schemas describing the syncing logic 
for each of the components that created a document result to be synced into Thoth database:

`solver <https://github.com/thoth-station/storages/tree/master/docs/>`_,
`package-analyzer <https://github.com/thoth-station/storages/tree/master/docs/>`_,
`package-extract <https://github.com/thoth-station/storages/tree/master/docs/>`_,
`adviser <https://github.com/thoth-station/storages/tree/master/docs/thoth_sync_adviser.jpg>`_,
`provenance-checker <https://github.com/thoth-station/storages/tree/master/docs/syncs/thoth_sync_provenance_checker.jpg>`_,
`dependency-monkey <https://github.com/thoth-station/storages/tree/master/docs/>`_ and
`inspection <https://github.com/thoth-station/storages/tree/master/docs/thoth_sync_amun.jpg>`_,

You can also see the schema for all components that syncs and create Python Packages in Thoth database `here <https://github.com/thoth-station/storages/tree/master/docs/thoth_syncs_togheter.jpg>`_.

All schemas are created using `yEd <https://www.yworks.com/products/yed>`_ freely available online.