Query Name Convention in Thoth


| Type | TemplateQuery | Output |
| --- | --- | --- |
| 1 | ``get_<objects>_all()`` Get all records of an entity and each record output will have attributes which depend on the entity (no constraint on that), therefore we have can string or a Tuple of strings in the List. | ``List[Any]`` |