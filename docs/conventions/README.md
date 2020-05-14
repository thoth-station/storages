Thoth storages definitions and rules for query name convention in Thoth
------------------------------------------------------------

- ``objects`` can be identified with Tuple of  strings containing attribute values of the object or by a single string matching the only attribute we are interested in.
E.g. Python package is an object made of a Tuple(name, version, url)

- ``python_package`` used in query is equivalent to ``python_package_version_entity`` looking at Thoth Knowledge Graph schema.

- ``attribute_name`` is the attribute of the object we want to use to group results.

- The model which are referring to users are identified with ``External`` in the Thoth Knowledge Graph schema. The flag ``is_external`` needs to be included in the query when we want to query for an object.

- All queries with output different from ``int`` shall have ``start_offset=0``, ``count=_DEFAULT_COUNT``, for pagination purposes.

- ``distinct`` is a flag introduced to have distinct values in the query result.

- Filters can have a default value of ``None`` which will disable them.

- Keep Python package tuples positional arguments.


Query Name Template in Thoth
----------------------------

| Type | TemplateQuery | Output |
| --- | --- | --- |
| 1 | ``get_<objects>_all()`` Get all records of an entity and each record output will have attributes which depend on the entity (no constraint on that), therefore we can have string or a Tuple of strings in the List. | ``List[Any]`` |
| 2 | ``get_<objects>_all_<attribute_filter>()`` It’s an extension of Type 1. Get all records of an entity grouped by an attribute of the entity and each record output will have attributes which depend on the entity (no constraint on that), therefore we can have string or a Tuple of strings in the List. | ``Dict[str, List[Any]]`` |
| 3 | ``get_<objects>_count()`` Get number of records count of an entity. The entity can be identified with Tuple of  strings containing attributes values of the entity. It depends on what we mean by the entity (e.g. Python Package is a Tuple(name, version, url). | ``Dict[str, int] or Dict[List[Any], int]]`` |
| 4 | ``get_<objects>_per_<attribute_filter>()`` Get records count of an entity. The entity can be identified with Tuple of  strings containing attributes values of the entity. It depends on what we mean by the entity (e.g. Python Package is a Tuple(name, version, url). | ``Dict[str, List[Any]]`` |
| 5 | ``get_<objects>_count_per_<attribute_filter>()`` It’s a particular case of type 3. Get number of  records count of an entity grouped by an attribute value. The entity can be identified with Tuple of  strings containing attributes values of the entity except the attribute used to group. It depends on what we mean by the entity (e.g. Python Package entity grouped by url will have a Tuple(name, version). | ``Dict[str, Dict[List[Any], int]] or Dict[str, Dict[str, int]]`` |
| 6 | ``get_<objects>_count_all()`` Count all records for a specific entity. | ``int`` |
| 7 | ``get_<object>()`` Get a specific record according to the input parameters in the function.. | ``Dict[str,Any] or List[str]`` |
| 8 | ``<object>_exists()`` Query to check if a specific record with specific attributes exists in the database. | ``bool`` |
| 9 | ``has_<object><statement>()`` Query to check if a specific record has a specific value of an attribute. | ``bool`` |
| 10 | ``is_<object><flag/statement>`` Returns boolean value indicating the value of the flag or statement. | ``bool`` |
