# Changelog for Thoth's Storage Module

## [0.1.0] - 2018-Jul-17 - goern

### Fixed

Make slash after prefix explicit, [#59](https://github.com/thoth-station/storages/pull/59)

## [0.0.33] - 2018-Jul-01 - goern

### Changed

Coala now has a max_line_lenght of 120, some unneeded E501 have been removed.

## [0.0.30] - 2018-Jun-26 - goern

### Added

Starting with this release we have a Zuul-CI pipeline that:

* lints on Pull Requrest and gate/merge

## Release 0.5.3 (2018-10-11T16:13:37)
* Automatic update of dependency boto3 from 1.9.19 to 1.9.21
* using envvar that are injected by OpenShift to discover janusgraph servcie host and port, this requires that a service called "janusgraph" is created
* Automatic update of dependency boto3 from 1.9.16 to 1.9.19
* Automatic update of dependency pytest from 3.8.1 to 3.8.2
* Automatic update of dependency boto3 from 1.9.15 to 1.9.16
* Update README file
* Automatic update of dependency boto3 from 1.9.14 to 1.9.15
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Introduce query for gathering dependencies
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Automatic update of dependency boto3 from 1.9.11 to 1.9.14
* Introduce method for gathering python package versions
* Introduce observation models and adapter
* Specify Python index from which the package came from
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Automatic update of dependency boto3 from 1.9.10 to 1.9.11
* Automatic update of dependency boto3 from 1.9.9 to 1.9.10
* Introduce check whether the given Python package exists
* Automatic update of dependency pytest from 3.7.3 to 3.8.1
* Automatic update of dependency boto3 from 1.8.3 to 1.9.9
* Automatic update of dependency pytest-cov from 2.5.1 to 2.6.0
* Automatic update of dependency thoth-common from 0.2.4 to 0.3.1
* Automatic update of dependency moto from 1.3.4 to 1.3.6
* Update janusgraph.py
* Sync debian packages to the graph database

## Release 0.5.4 (2018-10-12T09:14:50)
* Edge property is not a vertex property
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.11
* Automatic update of dependency boto3 from 1.9.21 to 1.9.22

## Release 0.6.0 (2018-10-22T10:43:00)
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* fixing project.post.jobs.trigger-build.vars.webhook_url
* Automatic update of dependency boto3 from 1.9.27 to 1.9.28
* Automatic update of dependency boto3 from 1.9.26 to 1.9.27
* Automatic update of dependency requests from 2.19.1 to 2.20.0
* Automatic update of dependency boto3 from 1.9.25 to 1.9.26
* Automatic update of dependency boto3 from 1.9.24 to 1.9.25
* Automatic update of dependency pytest from 3.8.2 to 3.9.1
* Automatic update of dependency boto3 from 1.9.23 to 1.9.24
* Add timestamp to the result schema
* Automatic update of dependency cython from 0.28.5 to 0.29
* Automatic update of dependency boto3 from 1.9.22 to 1.9.23

## Release 0.7.0 (2018-10-30T22:37:43)
* Use job id as document id instead of pod id
* Implement image lookup for fast checks of image analyses
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Automatic update of dependency pytest from 3.9.2 to 3.9.3
* Automatic update of dependency boto3 from 1.9.32 to 1.9.33
* Automatic update of dependency boto3 from 1.9.30 to 1.9.32
* Automatic update of dependency boto3 from 1.9.29 to 1.9.30
* Automatic update of dependency pytest from 3.9.1 to 3.9.2
* Automatic update of dependency boto3 from 1.9.28 to 1.9.29
* Remove ignore comments
* Fix CI

## Release 0.7.1 (2018-10-31T00:40:59)
* Fix wrong base class

## Release 0.7.2 (2018-10-31T12:22:42)


## Release 0.7.3 (2018-11-07T10:04:34)
* Automatic update of dependency boto3 from 1.9.38 to 1.9.39
* Automatic update of dependency boto3 from 1.9.37 to 1.9.38
* Introduce dependency monkey reports adapter
* Fix query to retrieve all package versions
* Exclude test directory
* Automatic update of dependency moto from 1.3.6 to 1.3.7
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* Fix document naming
* Fix CI failures
* Rename error flags
* Introduce unparsed flag
* Introduce unparsed flag
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* Keep schema up2date with recent schema changes
* Hostname is not equal to document id
* Introduce methods for checking unsolvable and unparsed packages
* Automatic update of dependency boto3 from 1.9.36 to 1.9.37
* Introduce transitive dependencies gathering method
* Normalize names of packages that are inserted into graph database
* Automatic update of dependency boto3 from 1.9.35 to 1.9.36
* Automatic update of dependency uvloop from 0.11.2 to 0.11.3
* Automatic update of dependency boto3 from 1.9.34 to 1.9.35

## Release 0.7.4 (2018-11-07T13:17:46)
* Fix unparseable solver result sync

## Release 0.7.5 (2018-11-08T10:43:48)
* Use common date utilities for creating datetime from timestamp
* Fix queries to janusgraph - aggregate by document ids
* Add method for counting documents
* Add methods in janusgraph for metrics
* Automatic update of dependency boto3 from 1.9.39 to 1.9.40
* Correctly handle decorator wrappers

## Release 0.7.6 (2018-11-08T13:09:47)
* Fix indentation error

## Release 0.8.0 (2018-11-15T12:22:25)
* Automatic update of dependency boto3 from 1.9.44 to 1.9.45
* Automatic update of dependency pytest from 3.10.1 to 4.0.0
* Automatic update of dependency boto3 from 1.9.43 to 1.9.44
* Add a query to check for solved packages
* Automatic update of dependency boto3 from 1.9.42 to 1.9.43
* Automatic update of dependency pytest from 3.10.0 to 3.10.1
* Automatic update of dependency boto3 from 1.9.41 to 1.9.42
* Automatic update of dependency boto3 from 1.9.40 to 1.9.41
* Automatic update of dependency requests from 2.20.0 to 2.20.1
* Extend quieries to janusgraph
* Extend quieries to janusgraph
* Fix return values
* Make sure to hit indexes with queries
* Fix indentation error

## Release 0.9.0 (2018-11-28T05:50:14)
* Corrected README file
* Update README to include test suite in setup.py
* Introduce query for gathering sha256 hashes
* Hashes are positional argument
* Create digest entries in the graph database for python packages
* Automatic update of dependency boto3 from 1.9.50 to 1.9.51
* Add long description for PyPI
* Use index_url in the graph database
* Sync indexes into the graph database
* Update schema document
* Introduce has_artifact edge
* Artifact hashes in graph database
* Automatic update of dependency cython from 0.29 to 0.29.1
* Automatic update of dependency pytest from 4.0.0 to 4.0.1
* Use base image name if there were not installed any native pkgs
* Report which inspection id is being synced
* Improve handling of performance index
* Hardware can be even None
* Fix key error if hardware was not provided on Amun
* Log about Amun results gathering
* Introduce graceful flag for inspection syncs
* Return directly list, not chain iterable
* Use models to_dict method to obtain values
* Fix Python package index URL retrieval
* Add method for retrieving Python package index URLs
* Update schema in docs
* Sync also performance index to janusgraph
* Introduce query for computing performance index
* Introduce method for registering Python package indexes
* Do not forget to install Amun client
* Introduce method for syncing inspection documents
* Automatic update of dependency boto3 from 1.9.49 to 1.9.50
* Gather performance index from inspection jobs
* Update schema docs
* Remove runtime and buildtime observations
* Fix recent errors
* Fix errors
* Fix syntax error
* Create method for syncing inspections into janusgraph
* Be consistent with storage prefix naming
* Rename observation_document_id to inspection_document_id
* Introduce buildtime environment model
* Fix CI
* Automatic update of dependency boto3 from 1.9.48 to 1.9.49
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Fix CI
* Do not use schema for inspections
* Remove unused variable
* Introduce sync methods
* Fix CI
* Adjust document_id gathering
* Introduce adapter for inspection results
* Introduce methods for checking documents based on id
* fixed some coala problems
* added a pyproject.toml to keep black happy
* using thoth's coala job
* using thoth-pytest job
* Fix pytest4 warning
* Return also python package index model
* Introduce method for creating Python package index vertex
* Update schema documentation
* Add python package index entity
* Automatic update of dependency boto3 from 1.9.47 to 1.9.48
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Automatic update of dependency boto3 from 1.9.46 to 1.9.47
* Automatic update of dependency pytest-timeout from 1.3.2 to 1.3.3
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Automatic update of dependency boto3 from 1.9.45 to 1.9.46
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1

## Release 0.9.1 (2018-12-03T13:33:36)
* Do not forget to install Amun for interaction with Amun
* Automatic update of dependency boto3 from 1.9.55 to 1.9.57
* Fixes for CI
* Automatic update of dependency amun from 0.1.3 to 0.2.0
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency boto3 from 1.9.51 to 1.9.55
* Consider index when retrieving transitive dependencies
* Include index url in the releases listing

## Release 0.9.4 (2018-12-12T00:30:21)
* Aggregate hashes from the graph database for the given package
* Automatic update of dependency requests from 2.20.1 to 2.21.0
* Automatic update of dependency boto3 from 1.9.61 to 1.9.62
* Automatic update of dependency boto3 from 1.9.60 to 1.9.61
* Automatic update of dependency boto3 from 1.9.59 to 1.9.60
* Automatic update of dependency boto3 from 1.9.58 to 1.9.59
* Performance index cannot be passed as None
* Normalize python package names before every graph operation
* Fix query
* Add index url to the check for Python package version existance
* Automatic update of dependency boto3 from 1.9.57 to 1.9.58
* Version 0.9.3
* Include also requirements-test.txt in package
* Version 0.9.2
* Include requirements.txt when packaging
* Release of version 0.9.1
* Do not forget to install Amun for interaction with Amun
* Automatic update of dependency boto3 from 1.9.55 to 1.9.57
* Fixes for CI
* Automatic update of dependency amun from 0.1.3 to 0.2.0
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency boto3 from 1.9.51 to 1.9.55
* Consider index when retrieving transitive dependencies
* Include index url in the releases listing
* Release of version 0.9.0
* Corrected README file
* Update README to include test suite in setup.py
* Introduce query for gathering sha256 hashes
* Hashes are positional argument
* Create digest entries in the graph database for python packages
* Automatic update of dependency boto3 from 1.9.50 to 1.9.51
* Add long description for PyPI
* Use index_url in the graph database
* Sync indexes into the graph database
* Update schema document
* Introduce has_artifact edge
* Artifact hashes in graph database
* Automatic update of dependency cython from 0.29 to 0.29.1
* Automatic update of dependency pytest from 4.0.0 to 4.0.1
* Use base image name if there were not installed any native pkgs
* Report which inspection id is being synced
* Improve handling of performance index
* Hardware can be even None
* Fix key error if hardware was not provided on Amun
* Log about Amun results gathering
* Introduce graceful flag for inspection syncs
* Return directly list, not chain iterable
* Use models to_dict method to obtain values
* Fix Python package index URL retrieval
* Add method for retrieving Python package index URLs
* Update schema in docs
* Sync also performance index to janusgraph
* Introduce query for computing performance index
* Introduce method for registering Python package indexes
* Do not forget to install Amun client
* Introduce method for syncing inspection documents
* Automatic update of dependency boto3 from 1.9.49 to 1.9.50
* Gather performance index from inspection jobs
* Update schema docs
* Remove runtime and buildtime observations
* Fix recent errors
* Fix errors
* Fix syntax error
* Create method for syncing inspections into janusgraph
* Be consistent with storage prefix naming
* Rename observation_document_id to inspection_document_id
* Introduce buildtime environment model
* Fix CI
* Automatic update of dependency boto3 from 1.9.48 to 1.9.49
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Fix CI
* Do not use schema for inspections
* Remove unused variable
* Introduce sync methods
* Fix CI
* Adjust document_id gathering
* Introduce adapter for inspection results
* Introduce methods for checking documents based on id
* fixed some coala problems
* added a pyproject.toml to keep black happy
* using thoth's coala job
* using thoth-pytest job
* Fix pytest4 warning
* Return also python package index model
* Introduce method for creating Python package index vertex
* Update schema documentation
* Add python package index entity
* Automatic update of dependency boto3 from 1.9.47 to 1.9.48
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Automatic update of dependency boto3 from 1.9.46 to 1.9.47
* Automatic update of dependency pytest-timeout from 1.3.2 to 1.3.3
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Automatic update of dependency boto3 from 1.9.45 to 1.9.46
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1
* Release of version 0.8.0
* Automatic update of dependency boto3 from 1.9.44 to 1.9.45
* Automatic update of dependency pytest from 3.10.1 to 4.0.0
* Automatic update of dependency boto3 from 1.9.43 to 1.9.44
* Add a query to check for solved packages
* Automatic update of dependency boto3 from 1.9.42 to 1.9.43
* Automatic update of dependency pytest from 3.10.0 to 3.10.1
* Automatic update of dependency boto3 from 1.9.41 to 1.9.42
* Automatic update of dependency boto3 from 1.9.40 to 1.9.41
* Automatic update of dependency requests from 2.20.0 to 2.20.1
* Extend quieries to janusgraph
* Release of version 0.7.6
* Extend quieries to janusgraph
* Fix return values
* Make sure to hit indexes with queries
* Fix indentation error
* Fix indentation error
* Release of version 0.7.5
* Use common date utilities for creating datetime from timestamp
* Fix queries to janusgraph - aggregate by document ids
* Add method for counting documents
* Add methods in janusgraph for metrics
* Automatic update of dependency boto3 from 1.9.39 to 1.9.40
* Release of version 0.7.4
* Fix unparseable solver result sync
* Release of version 0.7.3
* Correctly handle decorator wrappers
* Automatic update of dependency boto3 from 1.9.38 to 1.9.39
* Automatic update of dependency boto3 from 1.9.37 to 1.9.38
* Introduce dependency monkey reports adapter
* Fix query to retrieve all package versions
* Exclude test directory
* Automatic update of dependency moto from 1.3.6 to 1.3.7
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* Fix document naming
* Fix CI failures
* Rename error flags
* Introduce unparsed flag
* Introduce unparsed flag
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* Keep schema up2date with recent schema changes
* Hostname is not equal to document id
* Introduce methods for checking unsolvable and unparsed packages
* Automatic update of dependency boto3 from 1.9.36 to 1.9.37
* Introduce transitive dependencies gathering method
* Normalize names of packages that are inserted into graph database
* Automatic update of dependency boto3 from 1.9.35 to 1.9.36
* Automatic update of dependency uvloop from 0.11.2 to 0.11.3
* Automatic update of dependency boto3 from 1.9.34 to 1.9.35
* Release of version 0.7.2
* Introduce unsolvable flag
* Automatic update of dependency boto3 from 1.9.33 to 1.9.34
* Automatic update of dependency thoth-common from 0.3.15 to 0.3.16
* Release of version 0.7.1
* Fix wrong base class
* Release of version 0.7.0
* Use job id as document id instead of pod id
* Implement image lookup for fast checks of image analyses
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Automatic update of dependency pytest from 3.9.2 to 3.9.3
* Automatic update of dependency boto3 from 1.9.32 to 1.9.33
* Automatic update of dependency boto3 from 1.9.30 to 1.9.32
* Automatic update of dependency boto3 from 1.9.29 to 1.9.30
* Automatic update of dependency pytest from 3.9.1 to 3.9.2
* Automatic update of dependency boto3 from 1.9.28 to 1.9.29
* Release of version 0.6.0
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* fixing project.post.jobs.trigger-build.vars.webhook_url
* Automatic update of dependency boto3 from 1.9.27 to 1.9.28
* Automatic update of dependency boto3 from 1.9.26 to 1.9.27
* Automatic update of dependency requests from 2.19.1 to 2.20.0
* Automatic update of dependency boto3 from 1.9.25 to 1.9.26
* Automatic update of dependency boto3 from 1.9.24 to 1.9.25
* Automatic update of dependency pytest from 3.8.2 to 3.9.1
* Remove ignore comments
* Fix CI
* Automatic update of dependency boto3 from 1.9.23 to 1.9.24
* Add timestamp to the result schema
* Automatic update of dependency cython from 0.28.5 to 0.29
* Automatic update of dependency boto3 from 1.9.22 to 1.9.23
* Release of version 0.5.4
* Edge property is not a vertex property
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.11
* Automatic update of dependency boto3 from 1.9.21 to 1.9.22
* Release of version 0.5.3
* Automatic update of dependency boto3 from 1.9.19 to 1.9.21
* using envvar that are injected by OpenShift to discover janusgraph servcie host and port, this requires that a service called "janusgraph" is created
* Automatic update of dependency boto3 from 1.9.16 to 1.9.19
* Automatic update of dependency pytest from 3.8.1 to 3.8.2
* Automatic update of dependency boto3 from 1.9.15 to 1.9.16
* Update README file
* Automatic update of dependency boto3 from 1.9.14 to 1.9.15
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Introduce query for gathering dependencies
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Automatic update of dependency boto3 from 1.9.11 to 1.9.14
* Introduce method for gathering python package versions
* Introduce observation models and adapter
* Specify Python index from which the package came from
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Automatic update of dependency boto3 from 1.9.10 to 1.9.11
* Automatic update of dependency boto3 from 1.9.9 to 1.9.10
* Introduce check whether the given Python package exists
* Automatic update of dependency pytest from 3.7.3 to 3.8.1
* Automatic update of dependency boto3 from 1.8.3 to 1.9.9
* Automatic update of dependency pytest-cov from 2.5.1 to 2.6.0
* Automatic update of dependency thoth-common from 0.2.4 to 0.3.1
* Automatic update of dependency moto from 1.3.4 to 1.3.6
* Release of version 0.5.2
* Revert to the last release
* Revert "Release of version 0.5.6"
* Release of version 0.5.6
* Release of version 0.5.5
* Update .zuul.yaml
* Release of version 0.5.4
* Release of version 0.5.3
* Update janusgraph.py
* fixed line too long
* Sync debian packages to the graph database
* Release of version 0.5.2
* Automatic update of dependency thoth-common from 0.2.3 to 0.2.4
* Revert "put it in zuul's user-api queue"
* put it in zuul's user-api queue
* change the queue
* change the queue
* Create adapter for provenance reports
* Automatic update of dependency boto3 from 1.8.2 to 1.8.3
* Automatic update of dependency thoth-common from 0.2.2 to 0.2.3
* Release of version 0.5.1
* Store information about Python vulnerabilities
* Automatic update of dependency pytest-timeout from 1.3.1 to 1.3.2
* Automatic update of dependency boto3 from 1.8.1 to 1.8.2
* Fix missing import
* some pytest fixed wrt the prefix
* added VSCode directory to git ignore list
* some pylint fixed
* Automatic update of dependency pytest from 3.7.1 to 3.7.3
* Automatic update of dependency boto3 from 1.7.75 to 1.8.1
* Automatic update of dependency boto3 from 1.7.74 to 1.7.75
* Automatic update of dependency boto3 from 1.7.73 to 1.7.74
* Automatic update of dependency boto3 from 1.7.72 to 1.7.73
* Release of version 0.5.0
* Release of version 0.4.0
* Release of version 0.3.0
* Release of version 0.2.0
* Automatic dependency re-locking
* removing pylint, we dont need it and it leads to failing checks
* Update requirements.txt respecting requirements in Pipfile
* Release of version 0.1.1
* Fix key addresing
* releasing 0.1.0
* Make slash after prefix explicit
* Automatic update of dependency boto3 from 1.7.55 to 1.7.56
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Initial dependency lock
* Delete Pipfile.lock for relocking dependencies
* Automatic update of dependency boto3 from 1.7.52 to 1.7.54
* Automatic update of dependency cython from 0.28.3 to 0.28.4
* Automatic update of dependency thoth-common from 0.1.0 to 0.2.0
* Automatic update of dependency boto3 from 1.7.51 to 1.7.52
* Update .zuul.yaml
* removing pydocstyle
* preparing release 0.0.33
* removing unneeded E501
* Version 0.0.32
* Version 0.0.31
* Fix variable name
* added the gate pipeline to the core queue
* preparing for a zuul driven, fully coala compliant 0.0.30 release
* Change in variable names
* Change in indentation
* Query unsolved Runtime Environments from DB
* Use prefix with slash for Ceph
* rename ceph_host to s3_endpoint_url
* Skip python packages that do not have mercator result
* Package update
* Version 0.0.29
* Do not restrict Thoth packages
* Do not restrict Thoth packages
* Version 0.0.28
* Update thoth-common for rsyslog logging
* Use common datetime parsing handling
* Use PNG for images
* Version 0.0.27
* Modify requirements to fix yarl issues
* Ignore eggs in coala
* Run coala in non-interactive mode
* Make coala happy again
* Run coala in CI
* Run tests in Travis CI
* Version 0.0.26
* Add test dependencies
* Do not duplicate logic
* Test Ceph/S3 adapters against mocked environment
* Fix assertion test
* Update .gitignore
* Tests for cache
* Abstract common code to a base class
* Be consistent with indentation
* Different botocore versions behave differently
* Tests for Ceph adapter
* Test result schema
* No need to copy env variables
* Add base class for tests
* Rename failure test case for better readability
* Correctly propagate connection check to Ceph adapter
* Provide a way to specify bucket prefix explicitly
* Implement tests for build logs adapter
* Create initial tests
* Use coala for code checks
* Introduce Ceph connection check
* Fix yarl issues
* Expose adapter for adviser results
* Skip mercator errors that are not stored anyway
* Introduce adapter for adviser for recommendations
* Version 0.0.25
* Runtime environment analyses listing
* Version 0.0.24
* Remove unused import
* Version 0.0.23
* Return datetime instead of string
* Version 0.0.22
* Return used analysis document id
* Update thoth-common
* Method for retrieving analysis metadata
* Property can be None
* Improve error handling
* Check for object existence
* Preperly return property value
* Use __properties__ instead of __dict__
* Fix missing self reference
* Version 0.0.21
* Introduce to_pretty_dict() method
* Create a method for gathering runtime environment packages
* Version 0.0.20
* Introduce runtime environment listing method
* Create OWNERS
* Add license headers
* Use proper license in setup.py
* Use proper LICENSE file
* Version 0.0.19
* Introduce a method for retrieving dependent packages
* Provide a way to pass bucket prefix explicitly in constructor
* Fix issue with vertex property being stored instead of its value
* Introduce a function to find PyPI packages that deps were not resolved
* Add README file
* Version 0.0.18
* Introduce logic that wraps PyPI package creation
* Version 0.0.17
* Provide routines to check solver results or analysis results presence
* Add spaces after equal sign
* Version range should be always stated
* Also state package name on depends_on edge
* Filter out irrelevant artifact requirements.txt from sync
* Version 0.0.16
* Fix wrong attribute reference
* Make sure we use correct attributes
* Version 0.0.15
* Fix wrong property name
* Add missing attributes during sync
* Revisit key error fix
* A temporary fix for mercator result being None
* Fix key error when syncing to graph database
* Fix ecosystem name
* Log exception instead of error
* Log correct variable
* Log exception instead of error
* Be more sensitive with sync errors
* Fix missing argument
* Fix property types
* Bump schema docs version
* Update schema docs
* Revisit graph sync
* Version 0.0.14
* Remove nested .gitignore
* Respect changes in schema renaming
* Fix error when syncing data to janusgraph with VertexProperty
* Fix wrong model name
* Package version is now package_version
* Package version is now package_version
* Unify property naming
* Schema documentation
* Use VertexProperty class for Vertex properties
* Fix behavior in Jupyter notebooks to respect env variables
* Improving Goblin's driver performance
* Make caching configurable
* Implement cache handling
* Provide a way to specify source_id/target_id explicitly
* Initial schema creation and graph sync
* Version 0.0.13
* Introduce bucket prefix env variable
* Version 0.0.12
* Provide version information properly
* Expose session to JanusGraph
* Version 0.0.11
* Prefix also captures trailing /
* Make prefix configurable for the Ceph adapter
* Add create classmethod to create graph adapter
* Version 0.0.10
* Adjust adapter docstring
* Expose Ceph adapter in package
* Expose retrieving blob method in Ceph adapter
* Version 0.0.9
* Goblin's from_dict requires __label__ to be present
* Return document id when storing results
* Version 0.0.8
* Expose document listing API
* Fix wrong parameter
* Version 0.0.7
* Add adapter for build logs
* Add method for iterating over results in Ceph
* Version 0.0.6
* Raise appropriate exception on non-existing key
* Abstract document_id handling logic
* Raise an exception on invalid schema
* Abstract prefix creation
* Version 0.0.5
* Do not create bucket on Ceph for now
* Use RESULT_TYPE field to distinguish between database adapters
* Add missing dependnecy - boto3
* Reuse logic from result store base adapter in solver result adapter
* Reuse logic in analysis adapter from result base adapter
* Create result base for storing raw results onto Ceph
* Require keyword arguments for constructor
* Create Ceph adapter
* State only direct requirements in requirements.txt
* Make the g object accessible for the graph access
* Use new create() methods to be consistent
* Add base classes for vertex and edges to cover common logic
* Version 0.0.4
* Rename JanusGraphDatabase to GraphDatabase
* Fix typo
* Update requirements.txt
* Create storage base class
* Version 0.0.3
* Add forgotten dependency
* Version 0.0.2
* Add result schema for analyzer results
* Version 0.0.1
* Add docstrings for result store methods.
* Add logic to iterate over available results
* Refactor code to export defaults
* Improve logging + refactor defaults
* State all packages in requirements file
* Do not check requirements hashes for now
* Fix docstring
* Add .gitignore
* Implement analysis results store adapter
* Implement solver results store adapter
* Implement disconnecting logic
* Implement graph storing logic for JanusGraph
* Create initial classes with interface
* Add .travis.yml configuration file
* Initial project import

## Release 0.9.5 (2018-12-17T14:33:27)
* Linter fixes
* Remove unused imports
* Introduce name for a software stack
* Do not query graph database if no id is provided
* Introduce query for querying software stacks
* Retrieve python package versions using asyncio
* Automatic update of dependency boto3 from 1.9.65 to 1.9.66
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Automatic update of dependency cython from 0.29.1 to 0.29.2
* Automatic update of dependency boto3 from 1.9.64 to 1.9.65
* ignoring some coala errors
* Reformat using black
* Extend performance query so it is more generic
* Assign index to all packages in inspection sync
* Do not handle exception twice
* Automatic update of dependency boto3 from 1.9.63 to 1.9.64
* Automatic update of dependency thoth-common from 0.4.6 to 0.5.0
* Automatic update of dependency boto3 from 1.9.62 to 1.9.63
