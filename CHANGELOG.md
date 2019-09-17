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

## Release 0.9.6 (2019-02-13T18:07:13)
* If adviser analysis was not succesfull no lockfile is provided
* Respect runtime environment in queries for direct dependencies
* Let callee preserve None values
* Consider hardware with no None values
* Automatic update of dependency boto3 from 1.9.84 to 1.9.91
* Automatic update of dependency pytest from 4.1.1 to 4.2.0
* Automatic update of dependency cython from 0.29.3 to 0.29.5
* Add platform specific features to the transitive query
* Adjust CVE query to include version range
* Default to dash if the CVE has no name assigned
* Fix wrong import
* It's already 2019
* Distinguish different software stacks by their types
* Introduce method for listing all py packages
* Make graph optional parameter to reduce number of connections
* Fix reference to Pipfile.lock in ther result
* Adjust schema document
* Introduce mechanism for syncing adviser results
* Guard disconnect in destructor
* Introduce adapter for storing caching analysis ids based on image digest
* Depends on has to take account also environment
* Method can be static
* Adjust schema to reflect the current implementation
* Adjust solver related parts of schema for platform specifc features
* Introduce method for gathering packages known to thoth based on index
* Provide method for solver name parsing
* Introduce flag exposing "existed" for Python package version
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Automatic update of dependency boto3 from 1.9.83 to 1.9.84
* Automatic update of dependency pytest from 4.0.2 to 4.1.1
* Automatic update of dependency boto3 from 1.9.73 to 1.9.83
* Automatic update of dependency cython from 0.29.2 to 0.29.3
* Automatic update of dependency uvloop from 0.11.3 to 0.12.0
* Automatic update of dependency pytest-cov from 2.6.0 to 2.6.1
* Automatic update of dependency flexmock from 0.10.2 to 0.10.3
* Perform only graph or ceph sync if requested
* Move OpenShift specific bits to OpenShift
* Do not rely in Gremlin queries for order of received items
* Fix typo in retrieve_dependencies(...) query
* Minor fixes in method signatures
* Disconnect in destructor
* Automatic update of dependency boto3 from 1.9.71 to 1.9.73
* Avoid goblin model details in output
* Update README.rst
* Automatic update of dependency boto3 from 1.9.67 to 1.9.71
* Automatic update of dependency boto3 from 1.9.66 to 1.9.67

## Release 0.9.7 (2019-03-18T10:03:56)
* Fix clash of runtime environment - model versus representing class
* Add type to queries to hit index
* Turn ram size into float to fix serialization/deserialization issues
* Use Sphinx for documentation
* Delete ceph.py.orig
* :bug: removed the trailing slash
* Fix coala warnings
* Automatic update of dependency boto3 from 1.9.98 to 1.9.101
* Fix solver error flag handling
* Add missing dot in Python version
* Respect errors in dependencies of packages
* Adjust query to track solver errors on the given runtime env
* Track solver_errors on depends_on edges
* Add missing ecosystem in query
* Remove duplicit definition
* fixing some coala errors
* black reformatted the file
* this part of the path is no longer required
* This repo requires Python 3.6
* Fix split count
* Fix solver name handling
* Add missing export from thoth.storages module
* Fix path to origin value of adviser and provenance-checker resutls
* Be consistent with property naming
* Update schema in docs
* Add CVE name when querying for CVEs
* Create relations between all the models in the graph database
* Introduce adviser error flag in user stack
* Introduce logic for syncing provenance check documents
* Adjust query to return unsolved packages for the given solver
* Update README with the most recent information about schema generation
* Increase number of lines per file
* Add python version and cuda version to graph schema
* Capture recommendation type in the graph model
* Introduce advised relationship
* Fix in markup
* State thoth-schema file path directly
* State automatic schema generation in README file

## Release 0.10.0 (2019-04-17T12:59:43)
* New functions for janusgraph
* update schema file
* Fix coala complains
* Adjust method signatures
* New Edge between PythonPackageVersion and PythonPackageIndex
* Be consistent with return type, return always nan
* Adjust performance query to respect runtime environment
* Update schema
* Error in query get_analyzer_documents_count()
* Add Thoth's configuration file
* Make runtime and buildtime environment names shared
* Distinguish between runtime and buildtime environment
* Remove duplicit method

## Release 0.11.0 (2019-04-24T19:25:42)
* :pushpin: Automatic update of dependency pydgraph from 1.0.3 to 1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.130 to 1.9.134
* Fix coala complains
* Return None if no entity was found for in query_one
* Implemented runtime_environment_analyses_listing method for Dgraph
* Fix issues reported by coala runs
* Remove failing test
* Reformat using black, fix some coala warnings
* Always return float when computing average performance
* Implement query for retrieving transitive dependencies
* Implement method for gathering average performance
* Fix python_sync_analysis
* Implemented retrieve_unsolved_pypi_packages method for Dgraph
* Implemented retrieve_dependent_packages method for Dgraph
* Add missing provenance checker name
* Implement get_python_package_tuples for Dgraph
* Obsolete also unsolved_runtime_environments
* Remove obsolete queries
* fix one check
* Fixed output after tests
* Implemented get_all_versions_python_package method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_solved_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_unsolvable_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Fix typos
* Implemented retrieve_unparsable_pypi_packages method for Dgraph
* Implemented get_all_python_package_version_hashes_sha256 method for Dgraph
* Add normalization for package_name
* Implemented python_package_exists method for Dgraph
* Implemented python_package_version_exists method for Dgraph
* Added ecoystem filter
* Implemented get_python_packages_for_index method for Dgraph
* Implemented get_python_packages method for Dgraph
* Implemented analysis_records_exist method for Dgraph
* Implemented solver_records_exist method for Dgraph
* Fix get_analysis_metadata function, sync_functions, models and graph schema
* Add Francesco to module authors
* Remove unused imports in dgraph.py implementation
* Implement method for gathering CVEs for Python packages
* Implement query for retrieving artifact hashes from database
* Add query for checking provenance checker document id presence
* Add query for checking presence of inspection runs
* Implement logic for querying for DependencyMonkey document presence
* Implement logic for checking image analysis run presence
* Implemment logic for checking if adviser run is present in db
* Fix query for checking solver document presence
* Fix query to retrieve solver count
* User software stack can have adviser or provenance-checker document id
* Implement query for retrieving image analysis count
* Implement query for retrieving solver error count
* Fix handling target UID for vertexes
* Implement runtime_environment_listing for Dgraph
* Retrieve read-only transaction for query operations
* minor change
* Sync also digests when syncing solver documents
* Add missing annotations to models
* Remove checks which are already present in _create_python_package_record
* Fix syncing dependencies found in solver documents
* Schema proposal for Dgraph
* Add register_python_package_index to Dgraph implementation
* Implemented get_all_python_packages_count method for Dgraph
* completed method for dgraph
* Introduce get_analysis_metadata for Dgraph
* Fix facets syntax when syncing edges dictionaries
* Introduce solver_document_id_exist method for Dgraph
* Minor code fixes
* Implement get_python_package_index_urls for Dgraph
* Improve schema handling
* Fix sync of edge sync - source and target should not be part of sync
* Switch to Dgraph

## Release 0.11.1 (2019-05-03T12:27:35)
* Fix computing edge hashes
* Created missing functions for Dgraph
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* :pushpin: Automatic update of dependency boto3 from 1.9.140 to 1.9.141
* :pushpin: Automatic update of dependency boto3 from 1.9.139 to 1.9.140
* :pushpin: Automatic update of dependency boto3 from 1.9.138 to 1.9.139
* :pushpin: Automatic update of dependency boto3 from 1.9.137 to 1.9.138
* :pushpin: Automatic update of dependency pydgraph from 1.1 to 1.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.136 to 1.9.137
* :pushpin: Automatic update of dependency boto3 from 1.9.135 to 1.9.136
* Normalize Python package names before inserting them into database
* Remove unused method
* :pushpin: Automatic update of dependency boto3 from 1.9.134 to 1.9.135

## Release 0.11.2 (2019-05-08T18:02:30)
* Introduce mechanism to avoid gRPC issues when serializing large stacks
* Implement query for retrieving information about build-time errors
* :pushpin: Automatic update of dependency boto3 from 1.9.143 to 1.9.144
* :pushpin: Automatic update of dependency boto3 from 1.9.142 to 1.9.143
* Minor fix to display correct release in title of docs html
* Reorganize Python package creation
* Increase back-off count
* Implement back-off for random time in case of concurent upsert writes
* Fix missing import causing issues in graph-sync-job
* :pushpin: Automatic update of dependency boto3 from 1.9.141 to 1.9.142

## Release 0.11.3 (2019-05-09T02:24:37)
* Provide method for buildtime environment listing
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency boto3 from 1.9.144 to 1.9.145

## Release 0.11.4 (2019-05-11T01:42:22)
* Fix normalization issue - normalize only package names
* :pushpin: Automatic update of dependency boto3 from 1.9.145 to 1.9.146
* :pushpin: Automatic update of dependency amun from 0.2.0 to 0.2.1
* An environment can have no analyses associated

## Release 0.12.0 (2019-05-20T11:38:12)
* Removed unusued functions
* Update schema, functions and design schema
* :pushpin: Automatic update of dependency boto3 from 1.9.150 to 1.9.151
* New UserHardwareInformation entity
* :pushpin: Automatic update of dependency boto3 from 1.9.149 to 1.9.150
* Update for Dgraph
* :pushpin: Automatic update of dependency boto3 from 1.9.148 to 1.9.149
* Check for cyclic dependencies in transitive query
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency boto3 from 1.9.147 to 1.9.148
* Fix number of overall results
* Fix wrong indentation in adviser results sync
* :pushpin: Automatic update of dependency boto3 from 1.9.146 to 1.9.147
* Correct typo
* Qute fields as they are stored as strings
* Enhance exception information to give better information
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0

## Release 0.13.0 (2019-05-20T12:34:32)
* Release of version 0.12.0
* Removed unusued functions
* Update schema, functions and design schema
* :pushpin: Automatic update of dependency boto3 from 1.9.150 to 1.9.151
* New UserHardwareInformation entity
* :pushpin: Automatic update of dependency boto3 from 1.9.149 to 1.9.150
* Update for Dgraph
* :pushpin: Automatic update of dependency boto3 from 1.9.148 to 1.9.149
* Check for cyclic dependencies in transitive query
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency boto3 from 1.9.147 to 1.9.148
* Fix number of overall results
* Fix wrong indentation in adviser results sync
* :pushpin: Automatic update of dependency boto3 from 1.9.146 to 1.9.147
* Correct typo
* Qute fields as they are stored as strings
* Enhance exception information to give better information
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* Release of version 0.11.4
* Fix normalization issue - normalize only package names
* :pushpin: Automatic update of dependency boto3 from 1.9.145 to 1.9.146
* :pushpin: Automatic update of dependency amun from 0.2.0 to 0.2.1
* An environment can have no analyses associated
* Release of version 0.11.3
* Provide method for buildtime environment listing
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency boto3 from 1.9.144 to 1.9.145
* Release of version 0.11.2
* Introduce mechanism to avoid gRPC issues when serializing large stacks
* Implement query for retrieving information about build-time errors
* :pushpin: Automatic update of dependency boto3 from 1.9.143 to 1.9.144
* :pushpin: Automatic update of dependency boto3 from 1.9.142 to 1.9.143
* Minor fix to display correct release in title of docs html
* Reorganize Python package creation
* Increase back-off count
* Implement back-off for random time in case of concurent upsert writes
* Fix missing import causing issues in graph-sync-job
* :pushpin: Automatic update of dependency boto3 from 1.9.141 to 1.9.142
* Release of version 0.11.1
* Fix computing edge hashes
* Created missing functions for Dgraph
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* :pushpin: Automatic update of dependency boto3 from 1.9.140 to 1.9.141
* :pushpin: Automatic update of dependency boto3 from 1.9.139 to 1.9.140
* :pushpin: Automatic update of dependency boto3 from 1.9.138 to 1.9.139
* :pushpin: Automatic update of dependency boto3 from 1.9.137 to 1.9.138
* :pushpin: Automatic update of dependency pydgraph from 1.1 to 1.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.136 to 1.9.137
* :pushpin: Automatic update of dependency boto3 from 1.9.135 to 1.9.136
* Normalize Python package names before inserting them into database
* Remove unused method
* :pushpin: Automatic update of dependency boto3 from 1.9.134 to 1.9.135
* Release of version 0.11.0
* :pushpin: Automatic update of dependency moto from 1.3.7 to 1.3.8
* :pushpin: Automatic update of dependency pydgraph from 1.0.3 to 1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.130 to 1.9.134
* Fix coala complains
* Return None if no entity was found for in query_one
* Implemented runtime_environment_analyses_listing method for Dgraph
* Fix issues reported by coala runs
* Remove failing test
* Reformat using black, fix some coala warnings
* Always return float when computing average performance
* Implement query for retrieving transitive dependencies
* Implement method for gathering average performance
* Fix python_sync_analysis
* Implemented retrieve_unsolved_pypi_packages method for Dgraph
* Implemented retrieve_dependent_packages method for Dgraph
* Add missing provenance checker name
* Implement get_python_package_tuples for Dgraph
* Obsolete also unsolved_runtime_environments
* Remove obsolete queries
* fix one check
* Fixed output after tests
* Implemented get_all_versions_python_package method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_solved_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_unsolvable_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Fix typos
* Implemented retrieve_unparsable_pypi_packages method for Dgraph
* Implemented get_all_python_package_version_hashes_sha256 method for Dgraph
* Add normalization for package_name
* Implemented python_package_exists method for Dgraph
* Implemented python_package_version_exists method for Dgraph
* Added ecoystem filter
* Implemented get_python_packages_for_index method for Dgraph
* Implemented get_python_packages method for Dgraph
* Implemented analysis_records_exist method for Dgraph
* Implemented solver_records_exist method for Dgraph
* Fix get_analysis_metadata function, sync_functions, models and graph schema
* Add Francesco to module authors
* Remove unused imports in dgraph.py implementation
* Implement method for gathering CVEs for Python packages
* Implement query for retrieving artifact hashes from database
* Add query for checking provenance checker document id presence
* Add query for checking presence of inspection runs
* Implement logic for querying for DependencyMonkey document presence
* Implement logic for checking image analysis run presence
* Implemment logic for checking if adviser run is present in db
* Fix query for checking solver document presence
* Fix query to retrieve solver count
* User software stack can have adviser or provenance-checker document id
* Implement query for retrieving image analysis count
* Implement query for retrieving solver error count
* Fix handling target UID for vertexes
* Implement runtime_environment_listing for Dgraph
* Retrieve read-only transaction for query operations
* minor change
* Sync also digests when syncing solver documents
* Add missing annotations to models
* Remove checks which are already present in _create_python_package_record
* Fix syncing dependencies found in solver documents
* Schema proposal for Dgraph
* Add register_python_package_index to Dgraph implementation
* Implemented get_all_python_packages_count method for Dgraph
* completed method for dgraph
* Introduce get_analysis_metadata for Dgraph
* Fix facets syntax when syncing edges dictionaries
* Introduce solver_document_id_exist method for Dgraph
* Minor code fixes
* Implement get_python_package_index_urls for Dgraph
* Improve schema handling
* Fix sync of edge sync - source and target should not be part of sync
* Switch to Dgraph
* Release of version 0.10.0
* New functions for janusgraph
* update schema file
* Fix coala complains
* Adjust method signatures
* New Edge between PythonPackageVersion and PythonPackageIndex
* Be consistent with return type, return always nan
* Adjust performance query to respect runtime environment
* Update schema
* Error in query get_analyzer_documents_count()
* Add Thoth's configuration file
* Make runtime and buildtime environment names shared
* Distinguish between runtime and buildtime environment
* Remove duplicit method
* Release of version 0.9.7
* Fix clash of runtime environment - model versus representing class
* Add type to queries to hit index
* Turn ram size into float to fix serialization/deserialization issues
* Use Sphinx for documentation
* Delete ceph.py.orig
* :bug: removed the trailing slash
* Fix coala warnings
* Automatic update of dependency boto3 from 1.9.98 to 1.9.101
* Fix solver error flag handling
* Add missing dot in Python version
* Respect errors in dependencies of packages
* Adjust query to track solver errors on the given runtime env
* Track solver_errors on depends_on edges
* Add missing ecosystem in query
* Remove duplicit definition
* fixing some coala errors
* black reformatted the file
* this part of the path is no longer required
* This repo requires Python 3.6
* Fix split count
* Fix solver name handling
* Add missing export from thoth.storages module
* Fix path to origin value of adviser and provenance-checker resutls
* Be consistent with property naming
* Update schema in docs
* Add CVE name when querying for CVEs
* Create relations between all the models in the graph database
* Introduce adviser error flag in user stack
* Introduce logic for syncing provenance check documents
* Adjust query to return unsolved packages for the given solver
* Update README with the most recent information about schema generation
* Increase number of lines per file
* Add python version and cuda version to graph schema
* Capture recommendation type in the graph model
* Introduce advised relationship
* Fix in markup
* State thoth-schema file path directly
* State automatic schema generation in README file
* Release of version 0.9.6
* If adviser analysis was not succesfull no lockfile is provided
* Respect runtime environment in queries for direct dependencies
* Let callee preserve None values
* Consider hardware with no None values
* Automatic update of dependency boto3 from 1.9.84 to 1.9.91
* Automatic update of dependency pytest from 4.1.1 to 4.2.0
* Automatic update of dependency cython from 0.29.3 to 0.29.5
* Add platform specific features to the transitive query
* Adjust CVE query to include version range
* Default to dash if the CVE has no name assigned
* Fix wrong import
* It's already 2019
* Distinguish different software stacks by their types
* Introduce method for listing all py packages
* Make graph optional parameter to reduce number of connections
* Fix reference to Pipfile.lock in ther result
* Adjust schema document
* Introduce mechanism for syncing adviser results
* Guard disconnect in destructor
* Introduce adapter for storing caching analysis ids based on image digest
* Depends on has to take account also environment
* Method can be static
* Adjust schema to reflect the current implementation
* Adjust solver related parts of schema for platform specifc features
* Introduce method for gathering packages known to thoth based on index
* Provide method for solver name parsing
* Introduce flag exposing "existed" for Python package version
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Automatic update of dependency boto3 from 1.9.83 to 1.9.84
* Automatic update of dependency pytest from 4.0.2 to 4.1.1
* Automatic update of dependency boto3 from 1.9.73 to 1.9.83
* Automatic update of dependency cython from 0.29.2 to 0.29.3
* Automatic update of dependency uvloop from 0.11.3 to 0.12.0
* Automatic update of dependency pytest-cov from 2.6.0 to 2.6.1
* Automatic update of dependency flexmock from 0.10.2 to 0.10.3
* Perform only graph or ceph sync if requested
* Move OpenShift specific bits to OpenShift
* Do not rely in Gremlin queries for order of received items
* Fix typo in retrieve_dependencies(...) query
* Minor fixes in method signatures
* Disconnect in destructor
* Automatic update of dependency boto3 from 1.9.71 to 1.9.73
* Avoid goblin model details in output
* Update README.rst
* Automatic update of dependency boto3 from 1.9.67 to 1.9.71
* Automatic update of dependency boto3 from 1.9.66 to 1.9.67
* Release of version 0.9.5
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
* Release of version 0.9.4
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

## Release 0.14.0 (2019-05-28T20:47:59)
* Ignore changelog file in coala, it's getting too large
* :pushpin: Automatic update of dependency boto3 from 1.9.156 to 1.9.157
* :pushpin: Automatic update of dependency boto3 from 1.9.155 to 1.9.156
* :pushpin: Automatic update of dependency boto3 from 1.9.154 to 1.9.155
* :pushpin: Automatic update of dependency boto3 from 1.9.153 to 1.9.154
* Provide better exception message on parsing error
* :pushpin: Automatic update of dependency boto3 from 1.9.152 to 1.9.153
* :pushpin: Automatic update of dependency boto3 from 1.9.151 to 1.9.152
* Release of version 0.13.0
* Release of version 0.12.0
* Removed unusued functions
* Update schema, functions and design schema
* :pushpin: Automatic update of dependency boto3 from 1.9.150 to 1.9.151
* New UserHardwareInformation entity
* :pushpin: Automatic update of dependency boto3 from 1.9.149 to 1.9.150
* Update for Dgraph
* :pushpin: Automatic update of dependency boto3 from 1.9.148 to 1.9.149
* Check for cyclic dependencies in transitive query
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency boto3 from 1.9.147 to 1.9.148
* Fix number of overall results
* Fix wrong indentation in adviser results sync
* :pushpin: Automatic update of dependency boto3 from 1.9.146 to 1.9.147
* Correct typo
* Qute fields as they are stored as strings
* Enhance exception information to give better information
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* Release of version 0.11.4
* Fix normalization issue - normalize only package names
* :pushpin: Automatic update of dependency boto3 from 1.9.145 to 1.9.146
* :pushpin: Automatic update of dependency amun from 0.2.0 to 0.2.1
* An environment can have no analyses associated
* Release of version 0.11.3
* Provide method for buildtime environment listing
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency boto3 from 1.9.144 to 1.9.145
* Release of version 0.11.2
* Introduce mechanism to avoid gRPC issues when serializing large stacks
* Implement query for retrieving information about build-time errors
* :pushpin: Automatic update of dependency boto3 from 1.9.143 to 1.9.144
* :pushpin: Automatic update of dependency boto3 from 1.9.142 to 1.9.143
* Minor fix to display correct release in title of docs html
* Reorganize Python package creation
* Increase back-off count
* Implement back-off for random time in case of concurent upsert writes
* Fix missing import causing issues in graph-sync-job
* :pushpin: Automatic update of dependency boto3 from 1.9.141 to 1.9.142
* Release of version 0.11.1
* Fix computing edge hashes
* Created missing functions for Dgraph
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* :pushpin: Automatic update of dependency boto3 from 1.9.140 to 1.9.141
* :pushpin: Automatic update of dependency boto3 from 1.9.139 to 1.9.140
* :pushpin: Automatic update of dependency boto3 from 1.9.138 to 1.9.139
* :pushpin: Automatic update of dependency boto3 from 1.9.137 to 1.9.138
* :pushpin: Automatic update of dependency pydgraph from 1.1 to 1.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.136 to 1.9.137
* :pushpin: Automatic update of dependency boto3 from 1.9.135 to 1.9.136
* Normalize Python package names before inserting them into database
* Remove unused method
* :pushpin: Automatic update of dependency boto3 from 1.9.134 to 1.9.135
* Release of version 0.11.0
* :pushpin: Automatic update of dependency moto from 1.3.7 to 1.3.8
* :pushpin: Automatic update of dependency pydgraph from 1.0.3 to 1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.130 to 1.9.134
* Fix coala complains
* Return None if no entity was found for in query_one
* Implemented runtime_environment_analyses_listing method for Dgraph
* Fix issues reported by coala runs
* Remove failing test
* Reformat using black, fix some coala warnings
* Always return float when computing average performance
* Implement query for retrieving transitive dependencies
* Implement method for gathering average performance
* Fix python_sync_analysis
* Implemented retrieve_unsolved_pypi_packages method for Dgraph
* Implemented retrieve_dependent_packages method for Dgraph
* Add missing provenance checker name
* Implement get_python_package_tuples for Dgraph
* Obsolete also unsolved_runtime_environments
* Remove obsolete queries
* fix one check
* Fixed output after tests
* Implemented get_all_versions_python_package method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_solved_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_unsolvable_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Fix typos
* Implemented retrieve_unparsable_pypi_packages method for Dgraph
* Implemented get_all_python_package_version_hashes_sha256 method for Dgraph
* Add normalization for package_name
* Implemented python_package_exists method for Dgraph
* Implemented python_package_version_exists method for Dgraph
* Added ecoystem filter
* Implemented get_python_packages_for_index method for Dgraph
* Implemented get_python_packages method for Dgraph
* Implemented analysis_records_exist method for Dgraph
* Implemented solver_records_exist method for Dgraph
* Fix get_analysis_metadata function, sync_functions, models and graph schema
* Add Francesco to module authors
* Remove unused imports in dgraph.py implementation
* Implement method for gathering CVEs for Python packages
* Implement query for retrieving artifact hashes from database
* Add query for checking provenance checker document id presence
* Add query for checking presence of inspection runs
* Implement logic for querying for DependencyMonkey document presence
* Implement logic for checking image analysis run presence
* Implemment logic for checking if adviser run is present in db
* Fix query for checking solver document presence
* Fix query to retrieve solver count
* User software stack can have adviser or provenance-checker document id
* Implement query for retrieving image analysis count
* Implement query for retrieving solver error count
* Fix handling target UID for vertexes
* Implement runtime_environment_listing for Dgraph
* Retrieve read-only transaction for query operations
* minor change
* Sync also digests when syncing solver documents
* Add missing annotations to models
* Remove checks which are already present in _create_python_package_record
* Fix syncing dependencies found in solver documents
* Schema proposal for Dgraph
* Add register_python_package_index to Dgraph implementation
* Implemented get_all_python_packages_count method for Dgraph
* completed method for dgraph
* Introduce get_analysis_metadata for Dgraph
* Fix facets syntax when syncing edges dictionaries
* Introduce solver_document_id_exist method for Dgraph
* Minor code fixes
* Implement get_python_package_index_urls for Dgraph
* Improve schema handling
* Fix sync of edge sync - source and target should not be part of sync
* Switch to Dgraph
* Release of version 0.10.0
* New functions for janusgraph
* update schema file
* Fix coala complains
* Adjust method signatures
* New Edge between PythonPackageVersion and PythonPackageIndex
* Be consistent with return type, return always nan
* Adjust performance query to respect runtime environment
* Update schema
* Error in query get_analyzer_documents_count()
* Add Thoth's configuration file
* Make runtime and buildtime environment names shared
* Distinguish between runtime and buildtime environment
* Remove duplicit method
* Release of version 0.9.7
* Fix clash of runtime environment - model versus representing class
* Add type to queries to hit index
* Turn ram size into float to fix serialization/deserialization issues
* Use Sphinx for documentation
* Delete ceph.py.orig
* :bug: removed the trailing slash
* Fix coala warnings
* Automatic update of dependency boto3 from 1.9.98 to 1.9.101
* Fix solver error flag handling
* Add missing dot in Python version
* Respect errors in dependencies of packages
* Adjust query to track solver errors on the given runtime env
* Track solver_errors on depends_on edges
* Add missing ecosystem in query
* Remove duplicit definition
* fixing some coala errors
* black reformatted the file
* this part of the path is no longer required
* This repo requires Python 3.6
* Fix split count
* Fix solver name handling
* Add missing export from thoth.storages module
* Fix path to origin value of adviser and provenance-checker resutls
* Be consistent with property naming
* Update schema in docs
* Add CVE name when querying for CVEs
* Create relations between all the models in the graph database
* Introduce adviser error flag in user stack
* Introduce logic for syncing provenance check documents
* Adjust query to return unsolved packages for the given solver
* Update README with the most recent information about schema generation
* Increase number of lines per file
* Add python version and cuda version to graph schema
* Capture recommendation type in the graph model
* Introduce advised relationship
* Fix in markup
* State thoth-schema file path directly
* State automatic schema generation in README file
* Release of version 0.9.6
* If adviser analysis was not succesfull no lockfile is provided
* Respect runtime environment in queries for direct dependencies
* Let callee preserve None values
* Consider hardware with no None values
* Automatic update of dependency boto3 from 1.9.84 to 1.9.91
* Automatic update of dependency pytest from 4.1.1 to 4.2.0
* Automatic update of dependency cython from 0.29.3 to 0.29.5
* Add platform specific features to the transitive query
* Adjust CVE query to include version range
* Default to dash if the CVE has no name assigned
* Fix wrong import
* It's already 2019
* Distinguish different software stacks by their types
* Introduce method for listing all py packages
* Make graph optional parameter to reduce number of connections
* Fix reference to Pipfile.lock in ther result
* Adjust schema document
* Introduce mechanism for syncing adviser results
* Guard disconnect in destructor
* Introduce adapter for storing caching analysis ids based on image digest
* Depends on has to take account also environment
* Method can be static
* Adjust schema to reflect the current implementation
* Adjust solver related parts of schema for platform specifc features
* Introduce method for gathering packages known to thoth based on index
* Provide method for solver name parsing
* Introduce flag exposing "existed" for Python package version
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Automatic update of dependency boto3 from 1.9.83 to 1.9.84
* Automatic update of dependency pytest from 4.0.2 to 4.1.1
* Automatic update of dependency boto3 from 1.9.73 to 1.9.83
* Automatic update of dependency cython from 0.29.2 to 0.29.3
* Automatic update of dependency uvloop from 0.11.3 to 0.12.0
* Automatic update of dependency pytest-cov from 2.6.0 to 2.6.1
* Automatic update of dependency flexmock from 0.10.2 to 0.10.3
* Perform only graph or ceph sync if requested
* Move OpenShift specific bits to OpenShift
* Do not rely in Gremlin queries for order of received items
* Fix typo in retrieve_dependencies(...) query
* Minor fixes in method signatures
* Disconnect in destructor
* Automatic update of dependency boto3 from 1.9.71 to 1.9.73
* Avoid goblin model details in output
* Update README.rst
* Automatic update of dependency boto3 from 1.9.67 to 1.9.71
* Automatic update of dependency boto3 from 1.9.66 to 1.9.67
* Release of version 0.9.5
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
* Release of version 0.9.4
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

## Release 0.14.1 (2019-06-06T11:56:25)
* :pushpin: Automatic update of dependency boto3 from 1.9.161 to 1.9.162
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency boto3 from 1.9.159 to 1.9.161
* Fix wrong variable reference
* Check if the given package in the given version was solved by specific solver
* Provide OS version and name as a string
* :pushpin: Automatic update of dependency boto3 from 1.9.158 to 1.9.159
* :pushpin: Automatic update of dependency boto3 from 1.9.157 to 1.9.158

## Release 0.14.2 (2019-06-24T11:46:23)
* Modified logic of the query to retrieve unsolved python packages for a given solver
* :pushpin: Automatic update of dependency boto3 from 1.9.173 to 1.9.174
* :pushpin: Automatic update of dependency pydgraph from 1.1.2 to 1.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.172 to 1.9.173
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* :pushpin: Automatic update of dependency boto3 from 1.9.171 to 1.9.172
* :pushpin: Automatic update of dependency boto3 from 1.9.170 to 1.9.171
* :pushpin: Automatic update of dependency boto3 from 1.9.169 to 1.9.170
* :pushpin: Automatic update of dependency boto3 from 1.9.168 to 1.9.169
* Use index for int values of performance indicators
* New tests for inspection schema check before sync
* :pushpin: Automatic update of dependency boto3 from 1.9.167 to 1.9.168
* code-style and new functions
* Update schema image for Thoth KG
* New sync logic for PI
* Update dgraph model schema for new parameters for PI
* :pushpin: Automatic update of dependency boto3 from 1.9.166 to 1.9.167
* :pushpin: Automatic update of dependency boto3 from 1.9.165 to 1.9.166
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* :pushpin: Automatic update of dependency boto3 from 1.9.164 to 1.9.165
* :pushpin: Automatic update of dependency pydgraph from 1.1.1 to 1.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.163 to 1.9.164
* :pushpin: Automatic update of dependency boto3 from 1.9.162 to 1.9.163
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11

## Release 0.14.3 (2019-06-25T21:29:35)
* PackageAnalysisResultsStore is added
* Introduce pagination and solver_name filter
* :pushpin: Automatic update of dependency boto3 from 1.9.174 to 1.9.175
* Document local Dgraph instance setup

## Release 0.14.4 (2019-07-08T13:28:06)
* Introduce retry exception on concurrent upsert writes
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency boto3 from 1.9.182 to 1.9.183
* :pushpin: Automatic update of dependency boto3 from 1.9.181 to 1.9.182
* :pushpin: Automatic update of dependency boto3 from 1.9.180 to 1.9.181
* :pushpin: Automatic update of dependency moto from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency boto3 from 1.9.179 to 1.9.180
* :star: alphabetically order the files
* :pushpin: Automatic update of dependency boto3 from 1.9.178 to 1.9.179
* :pushpin: Automatic update of dependency boto3 from 1.9.176 to 1.9.178
* :pushpin: Automatic update of dependency boto3 from 1.9.175 to 1.9.176

## Release 0.14.5 (2019-07-08T18:46:09)
* :dizzy: updated adapters for storing buillog analysis results and cache

## Release 0.14.6 (2019-07-08T20:48:45)
* :pushpin: Automatic update of dependency boto3 from 1.9.183 to 1.9.184
* Introduce method for creating Python package version entities

## Release 0.14.7 (2019-07-10T21:18:59)
* :pushpin: Automatic update of dependency boto3 from 1.9.185 to 1.9.186
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* Fix refactoring typo
* Parametrize `@cascade` by `only_known_index` parameter
* :pushpin: Automatic update of dependency boto3 from 1.9.184 to 1.9.185
* Require non-null `index_url` and `package_name`

## Release 0.14.8 (2019-07-16T12:49:49)
* Document schema hadnling in a living deployment
* Update dgraph.py
* Update README to show how to connect to the graph database from code
* Parametrize retrieval of unsolvable packages for the given solver

## Release 0.15.0 (2019-07-19T13:28:41)
* Fix typo in matrix
* Update schema based on updates to performance indicators
* Propagate OS information to runtime/buildtime environment nodes
* Update schema to capture os-release information
* Sync information about operating system captured in package-extract
* Update schema image respecting recent changes in PiMatmul
* Unify schema for creating performance indicators and their handling
* Fix vertex cache handling
* Add standard project template and code owners
* Regenerate schema
* Rename models and properties
* Add PythonFileDigest to schema documentation
* Introduce delete operation on top of models
* sync_package_analysis_documents

## Release 0.15.1 (2019-07-22T19:41:14)
* Fix default value to environment variable
* Fix handling of missing usage in the inspection documents when syncing
* Add checks for inspection document syncing
* State in the README file how to debug graph database queries
* Enable logging of graph database queries for debugging
* Fix handling of query filter

## Release 0.15.2 (2019-07-23T13:18:20)
* Queries are concurrent, not parallel
* Decrease transitive query depth to address serialization issues
* Inspection specification is a dictionary

## Release 0.16.0 (2019-07-25T11:29:31)
* Corrected voluptuous requirements for inspection schema:
* Modified Inspection schema
* Updated schema for PIConv
* Quote user input parts of the query in error message produced
* Query for package versions without error by default

## Release 0.17.0 (2019-07-30T09:08:20)
* Remove old test
* Fix handling of pytest arguments in setup.py
* Revert changes in docker-compose
* Remove unused dependencies
* Rewrite querying logic for transitive dependencies retrieval
* Avoid copies when retrieving transitive dependencies
* Optimize retrieval of transitive queries

## Release 0.18.0 (2019-07-31T09:58:23)
* New Dgraph function for PI
* Add PI for Conv1D and Conv2D for tensorflow

## Release 0.18.1 (2019-08-01T14:23:46)
* Solved conflict pinning to older version
* Corrected datatype-error for syncing

## Release 0.18.2 (2019-08-01T17:03:19)
* Added missing inspection schema checks for voluptuous

## Release 0.18.3 (2019-08-01T18:39:30)
* Release of version 0.18.2
* Added missing inspection schema checks for voluptuous
* Release of version 0.18.1
* Solved conflict pinning to older version
* Corrected datatype-error for syncing
* Release of version 0.18.0
* New Dgraph function for PI
* Add PI for Conv1D and Conv2D for tensorflow
* Release of version 0.17.0
* Remove old test
* Fix handling of pytest arguments in setup.py
* Revert changes in docker-compose
* Remove unused dependencies
* Rewrite querying logic for transitive dependencies retrieval
* Avoid copies when retrieving transitive dependencies
* Optimize retrieval of transitive queries
* sync package analyzer results
* Update schema to include package analyzer
* Release of version 0.16.0
* Corrected voluptuous requirements for inspection schema:
* Modified Inspection schema
* Updated schema for PIConv
* Quote user input parts of the query in error message produced
* Query for package versions without error by default
* Release of version 0.15.2
* Queries are concurrent, not parallel
* Decrease transitive query depth to address serialization issues
* Inspection specification is a dictionary
* Release of version 0.15.1
* Fix default value to environment variable
* Fix handling of missing usage in the inspection documents when syncing
* Add checks for inspection document syncing
* Release of version 0.15.0
* State in the README file how to debug graph database queries
* Enable logging of graph database queries for debugging
* Fix handling of query filter
* Fix typo in matrix
* Update schema based on updates to performance indicators
* Propagate OS information to runtime/buildtime environment nodes
* Update schema to capture os-release information
* Sync information about operating system captured in package-extract
* Update schema image respecting recent changes in PiMatmul
* Unify schema for creating performance indicators and their handling
* Fix vertex cache handling
* Add standard project template and code owners
* Regenerate schema
* Rename models and properties
* Add PythonFileDigest to schema documentation
* Introduce delete operation on top of models
* sync_package_analysis_documents
* Release of version 0.14.8
* Document schema hadnling in a living deployment
* Update dgraph.py
* Update README to show how to connect to the graph database from code
* Parametrize retrieval of unsolvable packages for the given solver
* Release of version 0.14.7
* :pushpin: Automatic update of dependency boto3 from 1.9.185 to 1.9.186
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* Fix refactoring typo
* Parametrize `@cascade` by `only_known_index` parameter
* :pushpin: Automatic update of dependency boto3 from 1.9.184 to 1.9.185
* Release of version 0.14.6
* :pushpin: Automatic update of dependency boto3 from 1.9.183 to 1.9.184
* Release of version 0.14.5
* Introduce method for creating Python package version entities
* :dizzy: updated adapters for storing buillog analysis results and cache
* Release of version 0.14.4
* Introduce retry exception on concurrent upsert writes
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* Require non-null `index_url` and `package_name`
* :pushpin: Automatic update of dependency boto3 from 1.9.182 to 1.9.183
* :pushpin: Automatic update of dependency boto3 from 1.9.181 to 1.9.182
* :pushpin: Automatic update of dependency boto3 from 1.9.180 to 1.9.181
* :pushpin: Automatic update of dependency moto from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency boto3 from 1.9.179 to 1.9.180
* :star: alphabetically order the files
* :pushpin: Automatic update of dependency boto3 from 1.9.178 to 1.9.179
* :pushpin: Automatic update of dependency boto3 from 1.9.176 to 1.9.178
* :pushpin: Automatic update of dependency boto3 from 1.9.175 to 1.9.176
* Release of version 0.14.3
* PackageAnalysisResultsStore is added
* Introduce pagination and solver_name filter
* :pushpin: Automatic update of dependency boto3 from 1.9.174 to 1.9.175
* Document local Dgraph instance setup
* Release of version 0.14.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* Modified logic of the query to retrieve unsolved python packages for a given solver
* :pushpin: Automatic update of dependency boto3 from 1.9.173 to 1.9.174
* :pushpin: Automatic update of dependency pydgraph from 1.1.2 to 1.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.172 to 1.9.173
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* :pushpin: Automatic update of dependency boto3 from 1.9.171 to 1.9.172
* :pushpin: Automatic update of dependency boto3 from 1.9.170 to 1.9.171
* :pushpin: Automatic update of dependency boto3 from 1.9.169 to 1.9.170
* :pushpin: Automatic update of dependency boto3 from 1.9.168 to 1.9.169
* Use index for int values of performance indicators
* New tests for inspection schema check before sync
* :pushpin: Automatic update of dependency boto3 from 1.9.167 to 1.9.168
* code-style and new functions
* Update schema image for Thoth KG
* New sync logic for PI
* Update dgraph model schema for new parameters for PI
* :pushpin: Automatic update of dependency boto3 from 1.9.166 to 1.9.167
* :pushpin: Automatic update of dependency boto3 from 1.9.165 to 1.9.166
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* :pushpin: Automatic update of dependency boto3 from 1.9.164 to 1.9.165
* :pushpin: Automatic update of dependency pydgraph from 1.1.1 to 1.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.163 to 1.9.164
* :pushpin: Automatic update of dependency boto3 from 1.9.162 to 1.9.163
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* Release of version 0.14.1
* :pushpin: Automatic update of dependency boto3 from 1.9.161 to 1.9.162
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency boto3 from 1.9.159 to 1.9.161
* Fix wrong variable reference
* Check if the given package in the given version was solved by specific solver
* Provide OS version and name as a string
* :pushpin: Automatic update of dependency boto3 from 1.9.158 to 1.9.159
* :pushpin: Automatic update of dependency boto3 from 1.9.157 to 1.9.158
* Release of version 0.14.0
* Ignore changelog file in coala, it's getting too large
* :pushpin: Automatic update of dependency boto3 from 1.9.156 to 1.9.157
* :pushpin: Automatic update of dependency boto3 from 1.9.155 to 1.9.156
* :pushpin: Automatic update of dependency boto3 from 1.9.154 to 1.9.155
* :pushpin: Automatic update of dependency boto3 from 1.9.153 to 1.9.154
* Provide better exception message on parsing error
* :pushpin: Automatic update of dependency boto3 from 1.9.152 to 1.9.153
* :pushpin: Automatic update of dependency boto3 from 1.9.151 to 1.9.152
* Release of version 0.13.0
* Release of version 0.12.0
* Removed unusued functions
* Update schema, functions and design schema
* :pushpin: Automatic update of dependency boto3 from 1.9.150 to 1.9.151
* New UserHardwareInformation entity
* :pushpin: Automatic update of dependency boto3 from 1.9.149 to 1.9.150
* Update for Dgraph
* :pushpin: Automatic update of dependency boto3 from 1.9.148 to 1.9.149
* Check for cyclic dependencies in transitive query
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency boto3 from 1.9.147 to 1.9.148
* Fix number of overall results
* Fix wrong indentation in adviser results sync
* :pushpin: Automatic update of dependency boto3 from 1.9.146 to 1.9.147
* Correct typo
* Qute fields as they are stored as strings
* Enhance exception information to give better information
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* Release of version 0.11.4
* Fix normalization issue - normalize only package names
* :pushpin: Automatic update of dependency boto3 from 1.9.145 to 1.9.146
* :pushpin: Automatic update of dependency amun from 0.2.0 to 0.2.1
* An environment can have no analyses associated
* Release of version 0.11.3
* Provide method for buildtime environment listing
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency boto3 from 1.9.144 to 1.9.145
* Release of version 0.11.2
* Introduce mechanism to avoid gRPC issues when serializing large stacks
* Implement query for retrieving information about build-time errors
* :pushpin: Automatic update of dependency boto3 from 1.9.143 to 1.9.144
* :pushpin: Automatic update of dependency boto3 from 1.9.142 to 1.9.143
* Minor fix to display correct release in title of docs html
* Reorganize Python package creation
* Increase back-off count
* Implement back-off for random time in case of concurent upsert writes
* Fix missing import causing issues in graph-sync-job
* :pushpin: Automatic update of dependency boto3 from 1.9.141 to 1.9.142
* Release of version 0.11.1
* Fix computing edge hashes
* Created missing functions for Dgraph
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* :pushpin: Automatic update of dependency boto3 from 1.9.140 to 1.9.141
* :pushpin: Automatic update of dependency boto3 from 1.9.139 to 1.9.140
* :pushpin: Automatic update of dependency boto3 from 1.9.138 to 1.9.139
* :pushpin: Automatic update of dependency boto3 from 1.9.137 to 1.9.138
* :pushpin: Automatic update of dependency pydgraph from 1.1 to 1.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.136 to 1.9.137
* :pushpin: Automatic update of dependency boto3 from 1.9.135 to 1.9.136
* Normalize Python package names before inserting them into database
* Remove unused method
* :pushpin: Automatic update of dependency boto3 from 1.9.134 to 1.9.135
* Release of version 0.11.0
* :pushpin: Automatic update of dependency moto from 1.3.7 to 1.3.8
* :pushpin: Automatic update of dependency pydgraph from 1.0.3 to 1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.130 to 1.9.134
* Fix coala complains
* Return None if no entity was found for in query_one
* Implemented runtime_environment_analyses_listing method for Dgraph
* Fix issues reported by coala runs
* Remove failing test
* Reformat using black, fix some coala warnings
* Always return float when computing average performance
* Implement query for retrieving transitive dependencies
* Implement method for gathering average performance
* Fix python_sync_analysis
* Implemented retrieve_unsolved_pypi_packages method for Dgraph
* Implemented retrieve_dependent_packages method for Dgraph
* Add missing provenance checker name
* Implement get_python_package_tuples for Dgraph
* Obsolete also unsolved_runtime_environments
* Remove obsolete queries
* fix one check
* Fixed output after tests
* Implemented get_all_versions_python_package method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_solved_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Implemented retrieve_unsolvable_pypi_packages method for Dgraph
* Add @normalize to flatten results
* Fix typos
* Implemented retrieve_unparsable_pypi_packages method for Dgraph
* Implemented get_all_python_package_version_hashes_sha256 method for Dgraph
* Add normalization for package_name
* Implemented python_package_exists method for Dgraph
* Implemented python_package_version_exists method for Dgraph
* Added ecoystem filter
* Implemented get_python_packages_for_index method for Dgraph
* Implemented get_python_packages method for Dgraph
* Implemented analysis_records_exist method for Dgraph
* Implemented solver_records_exist method for Dgraph
* Fix get_analysis_metadata function, sync_functions, models and graph schema
* Add Francesco to module authors
* Remove unused imports in dgraph.py implementation
* Implement method for gathering CVEs for Python packages
* Implement query for retrieving artifact hashes from database
* Add query for checking provenance checker document id presence
* Add query for checking presence of inspection runs
* Implement logic for querying for DependencyMonkey document presence
* Implement logic for checking image analysis run presence
* Implemment logic for checking if adviser run is present in db
* Fix query for checking solver document presence
* Fix query to retrieve solver count
* User software stack can have adviser or provenance-checker document id
* Implement query for retrieving image analysis count
* Implement query for retrieving solver error count
* Fix handling target UID for vertexes
* Implement runtime_environment_listing for Dgraph
* Retrieve read-only transaction for query operations
* minor change
* Sync also digests when syncing solver documents
* Add missing annotations to models
* Remove checks which are already present in _create_python_package_record
* Fix syncing dependencies found in solver documents
* Schema proposal for Dgraph
* Add register_python_package_index to Dgraph implementation
* Implemented get_all_python_packages_count method for Dgraph
* completed method for dgraph
* Introduce get_analysis_metadata for Dgraph
* Fix facets syntax when syncing edges dictionaries
* Introduce solver_document_id_exist method for Dgraph
* Minor code fixes
* Implement get_python_package_index_urls for Dgraph
* Improve schema handling
* Fix sync of edge sync - source and target should not be part of sync
* Switch to Dgraph
* Release of version 0.10.0
* New functions for janusgraph
* update schema file
* Fix coala complains
* Adjust method signatures
* New Edge between PythonPackageVersion and PythonPackageIndex
* Be consistent with return type, return always nan
* Adjust performance query to respect runtime environment
* Update schema
* Error in query get_analyzer_documents_count()
* Add Thoth's configuration file
* Make runtime and buildtime environment names shared
* Distinguish between runtime and buildtime environment
* Remove duplicit method
* Release of version 0.9.7
* Fix clash of runtime environment - model versus representing class
* Add type to queries to hit index
* Turn ram size into float to fix serialization/deserialization issues
* Use Sphinx for documentation
* Delete ceph.py.orig
* :bug: removed the trailing slash
* Fix coala warnings
* Automatic update of dependency boto3 from 1.9.98 to 1.9.101
* Fix solver error flag handling
* Add missing dot in Python version
* Respect errors in dependencies of packages
* Adjust query to track solver errors on the given runtime env
* Track solver_errors on depends_on edges
* Add missing ecosystem in query
* Remove duplicit definition
* fixing some coala errors
* black reformatted the file
* this part of the path is no longer required
* This repo requires Python 3.6
* Fix split count
* Fix solver name handling
* Add missing export from thoth.storages module
* Fix path to origin value of adviser and provenance-checker resutls
* Be consistent with property naming
* Update schema in docs
* Add CVE name when querying for CVEs
* Create relations between all the models in the graph database
* Introduce adviser error flag in user stack
* Introduce logic for syncing provenance check documents
* Adjust query to return unsolved packages for the given solver
* Update README with the most recent information about schema generation
* Increase number of lines per file
* Add python version and cuda version to graph schema
* Capture recommendation type in the graph model
* Introduce advised relationship
* Fix in markup
* State thoth-schema file path directly
* State automatic schema generation in README file
* Release of version 0.9.6
* If adviser analysis was not succesfull no lockfile is provided
* Respect runtime environment in queries for direct dependencies
* Let callee preserve None values
* Consider hardware with no None values
* Automatic update of dependency boto3 from 1.9.84 to 1.9.91
* Automatic update of dependency pytest from 4.1.1 to 4.2.0
* Automatic update of dependency cython from 0.29.3 to 0.29.5
* Add platform specific features to the transitive query
* Adjust CVE query to include version range
* Default to dash if the CVE has no name assigned
* Fix wrong import
* It's already 2019
* Distinguish different software stacks by their types
* Introduce method for listing all py packages
* Make graph optional parameter to reduce number of connections
* Fix reference to Pipfile.lock in ther result
* Adjust schema document
* Introduce mechanism for syncing adviser results
* Guard disconnect in destructor
* Introduce adapter for storing caching analysis ids based on image digest
* Depends on has to take account also environment
* Method can be static
* Adjust schema to reflect the current implementation
* Adjust solver related parts of schema for platform specifc features
* Introduce method for gathering packages known to thoth based on index
* Provide method for solver name parsing
* Introduce flag exposing "existed" for Python package version
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Automatic update of dependency boto3 from 1.9.83 to 1.9.84
* Automatic update of dependency pytest from 4.0.2 to 4.1.1
* Automatic update of dependency boto3 from 1.9.73 to 1.9.83
* Automatic update of dependency cython from 0.29.2 to 0.29.3
* Automatic update of dependency uvloop from 0.11.3 to 0.12.0
* Automatic update of dependency pytest-cov from 2.6.0 to 2.6.1
* Automatic update of dependency flexmock from 0.10.2 to 0.10.3
* Perform only graph or ceph sync if requested
* Move OpenShift specific bits to OpenShift
* Do not rely in Gremlin queries for order of received items
* Fix typo in retrieve_dependencies(...) query
* Minor fixes in method signatures
* Disconnect in destructor
* Automatic update of dependency boto3 from 1.9.71 to 1.9.73
* Avoid goblin model details in output
* Update README.rst
* Automatic update of dependency boto3 from 1.9.67 to 1.9.71
* Automatic update of dependency boto3 from 1.9.66 to 1.9.67
* Release of version 0.9.5
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
* Release of version 0.9.4
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

## Release 0.18.4 (2019-08-08T16:50:38)
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* :pushpin: Automatic update of dependency boto3 from 1.9.202 to 1.9.203
* Fix Package Analyzer results syncing
* Fixes Syncing of Package Extract results
* :pushpin: Automatic update of dependency boto3 from 1.9.201 to 1.9.202
* :pushpin: Automatic update of dependency boto3 from 1.9.200 to 1.9.201
* Fix key error 'python'
* :pushpin: Automatic update of dependency boto3 from 1.9.199 to 1.9.200

## Release 0.18.5 (2019-08-12T12:12:57)
* Introduce a flag to retrieve only solved packages
* Use Python package name normalization from thoth-python module
* :pushpin: Automatic update of dependency boto3 from 1.9.204 to 1.9.205
* :pushpin: Automatic update of dependency boto3 from 1.9.203 to 1.9.204

## Release 0.18.6 (2019-08-14T14:06:19)
* Provide method for counting number of unsolved Python packages
* Fix query for retrieving unsolved Python packages
* :pushpin: Automatic update of dependency boto3 from 1.9.206 to 1.9.207
* Minor changes to the function which returns unanalyzed packages
* Retrieve packages that are not analyzed by Package-Analyzer
* :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* :pushpin: Automatic update of dependency voluptuous from 0.11.5 to 0.11.7
* :pushpin: Automatic update of dependency boto3 from 1.9.205 to 1.9.206
* :pushpin: Automatic update of dependency thoth-python from 0.6.0 to 0.6.1

## Release 0.19.0 (2019-09-17T08:54:47)
* :pushpin: Automatic update of dependency pydgraph from 1.2.0 to 2.0.2
* :pushpin: Automatic update of dependency boto3 from 1.9.222 to 1.9.229
* Remove accidentally committed file
* Provide method for disabling and enabling Python package index
* Remove unused imports
* Add missing software stack relation to inspections
* Add missing import
* State how to print stats to logs in README file
* Log statistics of graph cache and memory cache if requested so
* :pushpin: Automatic update of dependency boto3 from 1.9.228 to 1.9.229
* :pushpin: Automatic update of dependency boto3 from 1.9.227 to 1.9.228
* Drop performance related query
* Add tests and adjust existing testsuite to respect cache flags
* :pushpin: Automatic update of dependency boto3 from 1.9.226 to 1.9.227
* Disable cache inserts by default as they are expensive
* upsert-like logic
* Updates for consistency
* Logic to sync inspection
* Increase lines allowed in a file
* Sync pacakge-analyzer results
* Sync system symbols detected by a package-extract
* Fix cache test
* Fix returned variable
* Check for solver errors before adding package to cache
* Remove debug warnings accidentally committed
* Start session with subtransactions enabled
* Be explicit about join
* Package version can have some of the values None
* Remove unique constraint
* Rewrite cache query to retrieved dependencies
* Remove unused parameters
* Raise NotFoundError if no records were found
* Adjust query for retrieving performance indicators
* :pushpin: Automatic update of dependency boto3 from 1.9.225 to 1.9.226
* :pushpin: Automatic update of dependency pydgraph from 2.0.1 to 2.0.2
* Count number of performance indicators based on framework
* Introduce method for counting performance indicator entries
* Implement method for listing analyses
* Implement method for getting analysis metadata
* Make methods which create data without starting transaction private
* Remove methods which should not be used outside of module
* Unify environment type handling
* Sync system symbols detected by a package-extract
* Do not maintain schema for performance indicators
* Minor fixes to make dependency monkey syncs work properly
* Fix invalid foreign key error on schema creation
* Reformat using black
* Substitute from_properties with get_or_create in performance models
* Introduce logic for syncing dependency-monkey documents
* Unify software stack creation handling
* Unify Python package version handling in PostgreSQL
* Move cache specific function to cache implementation
* Implement logic for syncing adviser results
* Fix typos
* Implement logic for syncing provenance checker results
* :pushpin: Automatic update of dependency boto3 from 1.9.224 to 1.9.225
* Implement logic for syncing package-extract results
* Fix property name
* Introduce a new query which is used by adviser to filter out based on indexes
* Fix coala complains
* Remove old schema files
* Switch to PostgreSQL
* :pushpin: Automatic update of dependency boto3 from 1.9.223 to 1.9.224
* :pushpin: Automatic update of dependency pydgraph from 1.2.0 to 2.0.1
* :pushpin: Automatic update of dependency boto3 from 1.9.222 to 1.9.223
* capture error
* updated schema
* Sync package analyzer error
* Add error flag to package analyzer run
* Remove index key
* Adjust tests to work with new implementation
* Do not raise exception, return None instead
* :pushpin: Automatic update of dependency boto3 from 1.9.221 to 1.9.222
* Call dgraph initialization
* Remove caching on top of Dgraph
* Remove accidentally committed file
* Mirror PostgreSQL with Dgraph for now
* PostgreSQL implementation
* Add statistics of queries to sqlite3 cache
* Optimize two queries into one and iterate over all configurations resolved
* Do not use slots as LRU cache wrappers fail
* Provide mechanism to clear in-memory cache
* Add entries to cache only if there were no solver errors
* Provide more information on cache statistics
* Use methodtools to properly handle lru cache on methods
* Provide adapter for storing and restoring graph cache in builds
* Use indexes and minor fixes
* Use sqlite3 as cache
* Introduce cache for caching results of well-used packages
* Adjust query for retrieving transitive dependencies
* Adjust syncing logic to new depends_on schemantics
* :pushpin: Automatic update of dependency boto3 from 1.9.220 to 1.9.221
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.219 to 1.9.220
* :pushpin: Automatic update of dependency boto3 from 1.9.218 to 1.9.219
* :pushpin: Automatic update of dependency boto3 from 1.9.217 to 1.9.218
* :pushpin: Automatic update of dependency boto3 from 1.9.216 to 1.9.217
* :pushpin: Automatic update of dependency boto3 from 1.9.215 to 1.9.216
* :pushpin: Automatic update of dependency boto3 from 1.9.214 to 1.9.215
* :pushpin: Automatic update of dependency boto3 from 1.9.213 to 1.9.214
* Add is_provided flag
* :pushpin: Automatic update of dependency boto3 from 1.9.212 to 1.9.213
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.211 to 1.9.212
* :pushpin: Automatic update of dependency boto3 from 1.9.210 to 1.9.211
* :pushpin: Automatic update of dependency boto3 from 1.9.209 to 1.9.210
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* :pushpin: Automatic update of dependency boto3 from 1.9.208 to 1.9.209
* :pushpin: Automatic update of dependency boto3 from 1.9.207 to 1.9.208
* Coala errors
* Store symbols
* Add models for versioned symbols and associated edges
