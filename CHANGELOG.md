# Changelog for Thoth's Storage Module

## Release 0.68.0 (2022-01-26T13:52:54)
* Change rpm_package to rpm_package_name
* Rename python_package to package_name and correct argument type
* Fix with_entities
* Modify query of containerized environments to get specific content

## Release 0.67.0 (2022-01-26T09:16:12)
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Fix typo
* Rename columns for software_environment table
* Modify column name in migration file
* Restore changes to automatically created files
* Rename thoth_s2i_* in database schema
* add break statement and remove unique slug constraint
* Small typo fix
* Fix missing links in docs
* Enable TLS verification

## Release 0.66.0 (2022-01-11T15:01:00)
* add query for number of software stacks maintained by kebechet
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment

## Release 0.65.0 (2022-01-05T08:25:11)
* Provide a method that counts number of Python package names
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment

## Release 0.64.0 (2022-01-04T08:55:54)
* Introduce a query for counting software environments

## Release 0.63.0 (2021-12-22T12:11:56)
* Introduce query for obtaining solver documents for the given package
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Fix returning date when creating filters
* Allow sorting and pagination of get_python_package_version_names_all

## Release 0.62.1 (2021-12-21T18:50:24)
* Fix condition to identify env vars
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment

## Release 0.62.0 (2021-12-21T12:49:44)
* Be consistent across library
* Make sure datetime returned is string
* Update thoth/storages/graph/postgres.py
* Extend output query with package extract id and date
* make Package Extract Run table image size column datatype BigInteger
* Update thoth/storages/graph/postgres.py
* Allow syncing non-Thoth env variables
* Introduce a query for obtaining environments used to solve a package
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Parametrize query obtaining software environments
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Fix v0.61.0 changelog computed (#2499)
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Update pyproject.toml to use Python 3.8
* Fix v0.61.0 changelog computed

## Release 0.61.0 (2021-11-30T14:24:51)
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Modified package_extract_version to analysis_document_id in purge_package_extract_documents query
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment

## Release 0.60.0 (2021-11-29T11:52:15)
* Allow querying module imports
* Obtain environment markers based on evaluation result
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Add missing types
* add kebechet to crossroads in docs

## Release 0.59.0 (2021-11-19T03:05:03)
* Add distinct option to method
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Use explicit exports
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Adjust flexmock import to respect new flexmock release notes

## Release 0.58.0 (2021-11-08T09:20:00)
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Removed the build_sphinx command to generate docs in README.rst
* Change variable name from s3 to ceph
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel-8 environment
* Add CVE link to CVE table
* Provide primitives for manipulating with CVE timestamp
* Add both envvar and direct init example
* Rephrase sentences
* Fix EOF
* Add data retrieval example

## Release 0.57.3 (2021-10-21T12:39:28)
* Do not use colon in overlays name (#2451)
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment
* Adjust query to return also additional solver rule information
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment
* Fix signature

## Release 0.57.2 (2021-10-18T10:37:08)
* Use update on conflict method

## Release 0.57.1 (2021-10-15T15:47:47)
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment
* Update method to register or update package index
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment

## Release 0.57.0 (2021-09-22T11:00:40)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet for the rhel:8 environment
* Revert removing index from join
* add ability to filter github app installations as well as delete them

## Release 0.56.0 (2021-09-14T07:32:02)
### Features
* Fix unsolved query causing stage ingestion to halt
* Change get_python_package_version_import_packages_all() output
* Correct down_revision of migration
* add runtime_environment_name to KebechetGithubInstallation
* add runtime_environment_name to KebechetGithubInstallation
* Release of version 0.54.2
* :arrow_up: Automatic update of dependencies by Kebechet
* Remove unused import
* Add packages and populate with module names
* Add packages and populate with module names
### Bug Fixes
* Raise if no matching package for the given import was found
### Improvements
* Fix get_solved_python_package_versions_software_environment_all method
* Provide a method for deleting index
* corrected with black for prow tests
* corrected with black for prow tests
### Non-functional
* Improve performance of the unsolved Python packages query

## Release 0.55.0 (2021-08-20T08:15:56)
### Features
* add runtime_environment_name to KebechetGithubInstallation
* add runtime_environment_name to KebechetGithubInstallation

## Release 0.54.2 (2021-08-18T08:48:39)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet (#2412)
* Remove unused import
### Non-functional
* Improve performance of the unsolved Python packages query

## Release 0.54.1 (2021-08-04T12:47:19)
### Features
* Set default value for only_if_package_seen (#2413)
* :arrow_up: Automatic update of dependencies by Kebechet

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

## Release 0.19.1 (2019-09-17T13:22:50)
* :pushpin: Automatic update of dependency thoth-python from 0.6.1 to 0.6.2
* Use more generic env variable names

## Release 0.19.2 (2019-09-17T15:11:07)
* Fix documentation for performance indicators
* Implemented CASCADE on delete for Foreign Keys

## Release 0.19.3 (2019-09-17T16:49:19)
* Disable connection pooling

## Release 0.19.4 (2019-09-18T07:11:52)
* Count and limit for advises can be nullable
* Increase advisory message for CVEs
* :pushpin: Automatic update of dependency boto3 from 1.9.229 to 1.9.230

## Release 0.19.5 (2019-09-18T16:47:17)
* Document how to dump and restore database in the running cluster
* Adjust logged message to inform about concurrent writes
* Randomize retrieval of unsolved Python packages
* New class methods for InspectionStore
* Fix unsolved Python packages query
* Adjust signature of method to respect its return value

## Release 0.19.6 (2019-09-23T06:50:42)
* Add missing migrations to requirements.txt file
* :pushpin: Automatic update of dependency pytest from 5.1.2 to 5.1.3
* :pushpin: Automatic update of dependency boto3 from 1.9.232 to 1.9.233
* :pushpin: Automatic update of dependency alembic from 1.1.0 to 1.2.0
* Normalize Python package versions before each insert or query
* :pushpin: Automatic update of dependency boto3 from 1.9.231 to 1.9.232
* Fix small typo
* Make sure devs update to most recent version before generating new versions
* Minor typo fixes in README file
* Make coala happy
* Use UTC when generating schema versions
* Generate initial schema using Alembic
* Start using Alembic for database migrations
* Add missing method used to register new packages in package releases
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency boto3 from 1.9.230 to 1.9.231

## Release 0.19.7 (2019-09-24T13:30:23)
* Fix path to alembic versions - it has changed recently
* Allow limit latest versions to be None
* :pushpin: Automatic update of dependency boto3 from 1.9.233 to 1.9.234
* Make solver name optional when retrieving unsolved packages
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* Introduce a check to verify the current database schema is up2date
* Drop also alembic version table
* Distribute alembic migrations with thoth-storages

## Release 0.19.8 (2019-09-27T07:46:58)
* New query: count software stacks per type
* :pushpin: Automatic update of dependency boto3 from 1.9.236 to 1.9.237
* New queries
* Update queries
* We use psql not pg_restore
* Show an example run how to create a local PostgreSQL instance
* :pushpin: Automatic update of dependency boto3 from 1.9.235 to 1.9.236
* Use podman-compose
* Log what is being synced during graph syncs
* State graphviz package as a dependency when generating schema images
* :pushpin: Automatic update of dependency alembic from 1.2.0 to 1.2.1
* :pushpin: Automatic update of dependency boto3 from 1.9.234 to 1.9.235

## Release 0.19.9 (2019-09-30T07:50:08)
* Fix testsuite with recent changes
* :pushpin: Automatic update of dependency pytest from 5.1.3 to 5.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.237 to 1.9.238
* Add duration to the result schema

## Release 0.19.10 (2019-10-21T16:24:47)
* Add update sync schema for PackageExtract
* Correct syncing issue
* Allow nullable software environemnts in the schema
* Fix multiple heads present
* Fix reference to variable in the query
* Fix signature of the private method - unsolved edge cases
* Fix query to retrieve number of unsolved packages
* Fix error when case 3 is not declared yet
* Created query for python package metadata for user-api
* Created and updated queries for analyzed packages
* :pushpin: Automatic update of dependency boto3 from 1.9.251 to 1.9.252
* :pushpin: Automatic update of dependency boto3 from 1.9.250 to 1.9.251
* Sync python interpreters
* :pushpin: Automatic update of dependency boto3 from 1.9.249 to 1.9.250
* New schema and sync in Solver for PythonPackageMetadata
* :pushpin: Automatic update of dependency boto3 from 1.9.248 to 1.9.249
* :pushpin: Automatic update of dependency boto3 from 1.9.247 to 1.9.248
* Queries for packages with error in solvers and adjust schema
* Increase lenght file
* :pushpin: Automatic update of dependency boto3 from 1.9.246 to 1.9.247
* Consistenly sync index_url and package_version
* Added dependency monkey schema
* Added schema for package extract
* Added schema for package-extract sync
* Added solver sync schema
* Fix linkage of artifacts in Python package version entities
* Created adviser sync schema
* Add thoth sync schema for Amun
* Added provenance checker sync and all components sync
* Created docs for syncs inside Thoth Database
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.3 to 0.6.4
* Queries for packages with error in solvers and adjust schema
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.9 to 1.3.10
* :pushpin: Automatic update of dependency boto3 from 1.9.245 to 1.9.246
* Updated and tested all solved/unsolved functions
* Created solver functions following  naming convention
* :pushpin: Automatic update of dependency boto3 from 1.9.244 to 1.9.245
* Add missing import
* Remove unused import
* Created is_external for PackageExtractRun
* Remove old file for Dgraph related tests
* State how to implement syncing logic for any workload job done in the cluster
* Raise not found error if the given Python index is not found
* :pushpin: Automatic update of dependency boto3 from 1.9.243 to 1.9.244
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* Update syncs
* Changed schema and Added new Tables
* Fix performance indicator name
* :pushpin: Automatic update of dependency pytest from 5.2.0 to 5.2.1
* :pushpin: Automatic update of dependency pytest-cov from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency boto3 from 1.9.242 to 1.9.243
* Update functions for metrics
* :pushpin: Automatic update of dependency pytest-cov from 2.7.1 to 2.8.0
* Add examples to docstrings
* :pushpin: Automatic update of dependency boto3 from 1.9.241 to 1.9.242
* Generate migration for new schema
* Add logic for syncing marker and extra
* :pushpin: Automatic update of dependency boto3 from 1.9.240 to 1.9.241
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* Convert function according to new naming convention
* Remove obsolete exception
* Expose sync_documents outside of module
* Minor fix to address typo
* Implement a generic approach to sync any document
* :pushpin: Automatic update of dependency boto3 from 1.9.239 to 1.9.240
* Sync duration
* Generalized module varibale for count
* Created functions for get_python_packages cases
* Correct outputs
* New python_package_versions_count functions
* Hide query
* Added distinct flag
* No NULL values for some PythonPackageVersion attributes
* New query
* get_python_package_version_count
* :pushpin: Automatic update of dependency boto3 from 1.9.238 to 1.9.239
* New queries for python packages

## Release 0.19.11 (2019-10-25T07:51:29)
* :pushpin: Automatic update of dependency pytest from 5.2.1 to 5.2.2
* :pushpin: Automatic update of dependency boto3 from 1.10.1 to 1.10.2
* :pushpin: Automatic update of dependency methodtools from 0.1.0 to 0.1.1
* :pushpin: Automatic update of dependency boto3 from 1.10.0 to 1.10.1
* Handle issues in a better way
* Introduce query for checking marker evaluation results
* Add support for extras in the Python package dependencies retrieval query
* Remove graph cache tests
* Introduce additional exception types for specific exceptions raised
* Drop cache support
* :pushpin: Automatic update of dependency boto3 from 1.9.253 to 1.10.0
* Add offset and count
* Increase max lines per file
* Get internal software & hardware environments
* Start using mypy for type checks
* Add missing provides-extra column to Python metadata
* Add missing columns to Python metadata
* :pushpin: Automatic update of dependency thoth-python from 0.6.4 to 0.6.5
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.3 to 2.8.4
* :pushpin: Automatic update of dependency boto3 from 1.9.252 to 1.9.253
* Generic webhook updated to trigger the build from zuul

## Release 0.19.12 (2019-10-25T21:32:13)
* Fixing the func argunment names
* Fixing the func argunment design
* consistency in using the variable force
* Fix index url issue, now properly
* Fix index_url key, now properly
* Fix version key dereference
* Fix index url key in new solvers implementation
* Increase lines per file in Coala configuration
* Query environment markers stored in the database

## Release 0.19.13 (2019-10-29T16:14:14)
* State maintainer and project url in setup.py
* Issue warning on connection to the database if schema is not up2date
* :pushpin: Automatic update of dependency boto3 from 1.10.3 to 1.10.4
* :pushpin: Automatic update of dependency boto3 from 1.10.2 to 1.10.3
* Query to retrieve ML frameworks names
* Correct query to get metadata for Python Package
* HasArtifact is linked with PythonPackageVersionEntity table
* Revert "Symbol-API"
* Drop unique constraint in depends_on table
* added the registry to look for pgweb
* added podman-compose to dev packages list
* :pushpin: Automatic update of dependency methodtools from 0.1.1 to 0.1.2
* Fix model assignment when syncing results of Python interpreters
* Updated .coafile to allow for longer files
* Coala errors
* More verbose errors, require all parameters
* Add api to get versioned symbols

## Release 0.19.14 (2019-10-29T20:28:31)
* Fix model for index url in the query
* Keep Python package tuples positional arguments
* Issue warning if the database schema is not initialized yet in connect

## Release 0.19.15 (2019-11-04T12:08:12)
* Relax fatal error on syncing unmatched metadata
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.1 to 0.4.2
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* Randomize retrievals of unanalyzed Python packages
* Randomize retrieval of unsolved Python packages
* Remove old pydgraph dependency
* :pushpin: Automatic update of dependency boto3 from 1.10.7 to 1.10.8
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.34.2 to 0.35.0
* :pushpin: Automatic update of dependency boto3 from 1.10.6 to 1.10.7
* :pushpin: Automatic update of dependency alembic from 1.2.1 to 1.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.5 to 1.10.6
* Introduce enum classes for safe API
* Turn off checking thoth module by mypy
* Start using mypy in strict mode
* Fix retrieval of Python digests query
* :pushpin: Automatic update of dependency boto3 from 1.10.4 to 1.10.5
* Update the schema
* Sync container image size

## Release 0.19.16 (2019-11-05T20:28:30)
* Cache some of the query results
* :pushpin: Automatic update of dependency python-dateutil from 2.8.1 to 2.8.0
* :pushpin: Automatic update of dependency boto3 from 1.10.8 to 1.10.9
* Fix query to CVE for a given python package version entity
* Graph database cache has been removed
* Sync documents from a local directory if requested

## Release 0.19.17 (2019-11-06T16:13:41)
* Minor changes
* Added MetadataDistutils, updated sync logic, schema docs, Tested syncs


## Release 0.19.18 (2019-11-08T16:26:18)
* Correct attribute for metadata Provides-Extra
* Fix bug in checking for dist key
* :pushpin: Automatic update of dependency thoth-python from 0.6.5 to 0.7.1
* :pushpin: Automatic update of dependency boto3 from 1.10.12 to 1.10.13


## Release 0.19.19 (2019-11-12T12:36:34)
* Fix wrong propagation of is_local flag
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.10 to 1.3.11
* :pushpin: Automatic update of dependency boto3 from 1.10.14 to 1.10.15
* Increase character length for keywords metadata
* :pushpin: Automatic update of dependency boto3 from 1.10.13 to 1.10.14

## Release 0.19.20 (2019-11-15T12:25:44)
* Adjust output query for metric
* Introduce ping method
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency boto3 from 1.10.17 to 1.10.18
* Optimized/Improved query to retrieve unsolved Python Packages
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* Fix schema check
* :pushpin: Automatic update of dependency boto3 from 1.10.16 to 1.10.17
* State ignoring a role assignment in docs
* :pushpin: Automatic update of dependency alembic from 1.3.0 to 1.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15

## Release 0.19.21 (2019-11-18T09:33:24)
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* :pushpin: Automatic update of dependency boto3 from 1.10.18 to 1.10.19
* Fix wrong rebase
* Dispose engine on disconnect
* Dispose engine on connect issues
* Use default pooling from sqlalchemy

## Release 0.19.22 (2019-11-18T15:41:20)
* Use same version as in the cluster

## Release 0.19.23 (2019-11-21T17:26:34)
* Remove self to make method static
* Use context manager for handling sessions
* :pushpin: Automatic update of dependency boto3 from 1.10.22 to 1.10.23
* :pushpin: Automatic update of dependency boto3 from 1.10.21 to 1.10.22
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.20 to 1.10.21
* :pushpin: Automatic update of dependency boto3 from 1.10.19 to 1.10.20
* Fix warning for migration configuration check
* Correct output of queries

## Release 0.19.24 (2019-11-22T17:44:38)
* Fix referencing store if is_local is set
* Add ability to sync documents based on absolute path
* :pushpin: Automatic update of dependency boto3 from 1.10.24 to 1.10.25
* :pushpin: Automatic update of dependency boto3 from 1.10.23 to 1.10.24

## Release 0.19.25 (2019-11-29T11:33:33)
* Adjust tests to the new implementation
* Increase characters metadata in keywords and summary metadata
* Optimized Solved quries with error
* Optimize Analyzed Python Packages queries
* Optimnize unsolved queries
* Optimize queries
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* Cache environment marker evaluation result
* :package: store database backup to ceph storage
* Fix Issue #1308 not iterable
* Fix alembic configuration instantiation issues
* Gather document id from document_id field
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* Use open instead of pathlib to adress PV in-cluster issues
* :pushpin: Automatic update of dependency boto3 from 1.10.26 to 1.10.27
* Make library thread safe
* Issue warning instead of error
* Introduced sorting type in queries
* :pushpin: Automatic update of dependency sqlalchemy-stubs from 0.2 to 0.3
* Fix wrong staticmethod
* :pushpin: Automatic update of dependency boto3 from 1.10.25 to 1.10.26
* :green_heart: added more builds that need to be triggered

## Release 0.19.26 (2019-12-05T20:48:02)
* Add Google Analytics
* Adjust testsuite
* Provide OS release schema
* Adjust default is_provided value
* Rename flag to is_provided_package_version
* Change Sphinx theme
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency boto3 from 1.10.32 to 1.10.33
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* :pushpin: Automatic update of dependency boto3 from 1.10.31 to 1.10.32
* :pushpin: Automatic update of dependency boto3 from 1.10.30 to 1.10.31
* Make some log info optional
* Correct staticmethod
* :pushpin: Automatic update of dependency boto3 from 1.10.29 to 1.10.30
* :pushpin: Automatic update of dependency pyyaml from 5.1.2 to 5.2
* :pushpin: Automatic update of dependency boto3 from 1.10.28 to 1.10.29
* Create index for get_depends_on query
* Do not sync package errors if the given package is not provided
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.19

## Release 0.19.27 (2019-12-06T10:22:57)
* UBI:8 has optional variant_id
* :pushpin: Automatic update of dependency boto3 from 1.10.33 to 1.10.34

## Release 0.19.28 (2019-12-09T12:05:30)
* Add Thamos documentation
* Document automatic graph-backup job
* More formatting changes
* Minor docs reformatting
* Show database schema
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.35.0 to 0.36.0
* Provide is_s2i flag for adviser runs
* Point documentation to other libraries
* Add aggregated_at column to CVE
* Select distinct CVEs
* Remove duplicate entry
* Adjust tests to new metadata
* Add deployment name to the result schema

## Release 0.19.29 (2019-12-17T13:14:08)
* Increment solver error cache
* :pushpin: Automatic update of dependency alembic from 1.3.1 to 1.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.39 to 1.10.40
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.11 to 1.3.12
* Increase cache for caching solver errors
* Introduce PyBench PI table and adjust sync logic for inspection
* Remove unused indexes in depends_on table
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.38 to 1.10.39
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency boto3 from 1.10.35 to 1.10.38
* Fix Automatic Update Failure
* Sync cuda version
* Add missing filter
* :pushpin: Automatic update of dependency boto3 from 1.10.34 to 1.10.35
* Generalize function to retrieve multi values key metadata
* Add platforms
* WIP: Adjust Python Package Metadata query

## Release 0.19.30 (2019-12-17T14:45:54)
* Release of version 0.19.29
* Increment solver error cache

## Release 0.20.0 (2020-01-02T10:14:17)
* Sync package version requested rather than package version reported
* Optimize marker evaluation result query for adviser
* :pushpin: Automatic update of dependency boto3 from 1.10.44 to 1.10.45
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.0 to 0.36.1
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency boto3 from 1.10.43 to 1.10.44
* Do not show alembic info on configure_logger
* :pushpin: Automatic update of dependency boto3 from 1.10.42 to 1.10.43
* Super has no __del__
* Do not dispose engine in destructor
* Log number of dumps maintained
* Adjust names of parameters to respect their semantics
* Implement rotation of backups
* Fixes in reStructuredText in README file
* :pushpin: Automatic update of dependency boto3 from 1.10.41 to 1.10.42
* :pushpin: Automatic update of dependency boto3 from 1.10.40 to 1.10.41

## Release 0.20.1 (2020-01-03T10:44:00)
* :sparkles: added a PR template
* Fix keyword argument passing
* :pushpin: Automatic update of dependency boto3 from 1.10.45 to 1.10.46

## Release 0.20.2 (2020-01-03T14:03:40)
* Happy new year!
* Remove string size limitations from depends_on table

## Release 0.20.3 (2020-01-06T10:03:33)
* Fix syncs in versions

## Release 0.20.4 (2020-01-06T13:33:55)
* Fix wrong argument name propagated

## Release 0.20.5 (2020-01-07T15:23:43)
* Adjust model performance for inspection output
* Correct key from inspection output
* correct typo
* Missing randomize
* Adjust to follow naming convention
* Introduce software environment specific queries
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.3 to 1.3.4
* :pushpin: Automatic update of dependency pyyaml from 5.2 to 5.3
* :pushpin: Automatic update of dependency boto3 from 1.10.46 to 1.10.47

## Release 0.20.6 (2020-01-07T19:25:30)
* Fix syncing external software environments coming from adviser
* Release of version 0.20.5

## Release 0.21.0 (2020-01-09T22:11:05)
* :pushpin: Automatic update of dependency thoth-python from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency boto3 from 1.10.48 to 1.10.49
* Use datetime to sort results
* Do not use id when counting tables
* Fix advised software stack sync
* :pushpin: Automatic update of dependency thoth-python from 0.8.0 to 0.9.0
* Format using black
* Drop id columns on relation tables
* Create index for CVE step to omit sequence scan
* :pushpin: Automatic update of dependency boto3 from 1.10.47 to 1.10.48

## Release 0.21.1 (2020-01-10T12:03:05)
* Fix parameter name for syncing provenance-checker documents
* Provide environment variable marker flag when retrieving transitive deps
* Adjust syncing logic of Dependency Monkey documents based on the current output
* Correct inspection sync key
* :pushpin: Automatic update of dependency amun from 0.2.7 to 0.3.0

## Release 0.21.2 (2020-01-10T13:56:29)
* Release of version 0.21.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* Fix parameter name for syncing provenance-checker documents
* Provide environment variable marker flag when retrieving transitive deps

## Release 0.21.3 (2020-01-10T19:14:53)
* Adjust datatype for conv PI to sync inspection results

## Release 0.21.4 (2020-01-13T09:26:49)
* Query for index_url before creating index
* Introduce a query for retrieving Python package entity names
* :pushpin: Automatic update of dependency boto3 from 1.10.50 to 1.11.0

## Release 0.21.5 (2020-01-13T11:28:50)
* Alembic didn't create correct change in schema
* Consider only enabled indexes in unsolved queries

## Release 0.21.6 (2020-01-13T21:21:13)
* Fix query for enabled index
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25

## Release 0.21.7 (2020-01-15T19:55:45)
* Introduce a way to parametrize memory cache size
* Create index for has_artifact table
* :pushpin: Automatic update of dependency boto3 from 1.11.1 to 1.11.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* Add index for solved table - it optimizes the has_solver_error query in adviser
* Adjust index for PPV combinations

## Release 0.21.8 (2020-01-21T00:14:12)
* :pushpin: Automatic update of dependency boto3 from 1.11.5 to 1.11.6
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* Adjust parameter in query for PI
* Correct datatype
* Add missing key to sync inspections
* Set Packages Extract flag is_external to True always
* Missing change in query name to follow created standards
* :pushpin: Automatic update of dependency boto3 from 1.11.4 to 1.11.5
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency amun from 0.3.2 to 0.3.3
* Normalize OS version by discarding any minor release in RHEL release string
* :pushpin: Automatic update of dependency boto3 from 1.11.3 to 1.11.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.28
* :sweat_smile: Auto pip and black formatting
* :pushpin: Automatic update of dependency amun from 0.3.1 to 0.3.2
* :pushpin: Automatic update of dependency boto3 from 1.11.2 to 1.11.3

## Release 0.21.9 (2020-01-21T02:05:51)
* Release of version 0.21.8
* :pushpin: Automatic update of dependency boto3 from 1.11.5 to 1.11.6
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* Adjust parameter in query for PI

## Release 0.21.10 (2020-01-21T14:48:25)
* Make keys Optional
* :pushpin: Automatic update of dependency amun from 0.3.3 to 0.3.4

## Release 0.21.11 (2020-01-27T11:22:03)
* Add missing keys to inspection schema validation
* :pushpin: Automatic update of dependency boto3 from 1.11.8 to 1.11.9
* :pushpin: Automatic update of dependency boto3 from 1.11.7 to 1.11.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.12 to 1.3.13
* :pushpin: Automatic update of dependency alembic from 1.3.2 to 1.3.3
* new GitHub templates
* added some files to gitignore
* :pushpin: Automatic update of dependency boto3 from 1.11.6 to 1.11.7
* :pushpin: Automatic update of dependency amun from 0.3.4 to 0.3.5
* Added build log analysis result observations to graph database

## Release 0.22.0 (2020-02-09T18:24:46)
* :pushpin: Automatic update of dependency boto3 from 1.11.12 to 1.11.13
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency boto3 from 1.11.11 to 1.11.12
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic update of dependency boto3 from 1.11.10 to 1.11.11
* Sync missing packages if adviser failed due to unknown dependencies
* Avoid one join in the query
* Fix package symbols query
* Set default to False to reduce logging
* Fix inspection syncing for RHEL
* Fix index creation for symbols queries
* Fix OS name synced in container image analysis
* No need to query for package extract run - software environment can be directly used
* :pushpin: Automatic update of dependency alembic from 1.3.3 to 1.4.0
* :pushpin: Automatic update of dependency boto3 from 1.11.9 to 1.11.10
* normalize, distinct, fix index
* Alembic update
* Change from externalsoftware environment, and uncouple id index
* Move cache to storage level
* Add indexes to improve abi queries
* Filter early
* outer join causing none values
* Refactor query for retrieving symbols in an image
* Make cuda version optional
* Simplified API functions
* Created query to monitor bloat data
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* Fix reference to variable
* Fix method call to serialize models
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* Fixed missing index issue
* :pushpin: Automatic update of dependency amun from 0.3.7 to 0.3.8
* :pushpin: Automatic update of dependency amun from 0.3.6 to 0.3.7
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency amun from 0.3.5 to 0.3.6

## Release 0.22.1 (2020-02-12T14:53:29)
* Add check in sync when report is not provided by Adviser
* :pushpin: Automatic update of dependency boto3 from 1.11.14 to 1.11.15
* Include models using `fullmatch` instead of `search`
* Added option to exclude models from generated schema
* :pushpin: Automatic update of dependency boto3 from 1.11.13 to 1.11.14
* Update .thoth.yaml

## Release 0.22.2 (2020-02-13T08:23:28)
* :pushpin: Automatic update of dependency boto3 from 1.11.15 to 1.11.16
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* All counts optional

## Release 0.22.3 (2020-02-25T12:48:07)
* Move import to local use
* :pushpin: Automatic update of dependency boto3 from 1.12.5 to 1.12.6
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.2 to 0.5.0
* :pushpin: Automatic update of dependency boto3 from 1.12.4 to 1.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.3 to 1.12.4
* :pushpin: Automatic update of dependency boto3 from 1.12.2 to 1.12.3
* Alembic update
* flag for missing package version
* :pushpin: Automatic update of dependency amun from 0.3.8 to 0.4.0
* :pushpin: Automatic update of dependency boto3 from 1.12.1 to 1.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.0 to 1.12.1
* Python must have major and minor version
* Change regex expression
* :pushpin: Automatic update of dependency boto3 from 1.11.17 to 1.12.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency boto3 from 1.11.16 to 1.11.17
* raise valueError
* Address issue #1573

## Release 0.22.4 (2020-03-19T23:20:03)
* :pushpin: Automatic update of dependency boto3 from 1.12.24 to 1.12.25
* Reduce number of queries for environment markers by caching results
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* :pushpin: Automatic update of dependency boto3 from 1.12.23 to 1.12.24
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.2 to 0.36.3
* :pushpin: Automatic update of dependency boto3 from 1.12.22 to 1.12.23
* upcase
* Add empty env template
* :pushpin: Automatic update of dependency boto3 from 1.12.21 to 1.12.22
* :pushpin: Automatic update of dependency pytest from 5.3.5 to 5.4.1
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.1 to 0.36.2
* :pushpin: Automatic update of dependency pytest-mypy from 0.5.0 to 0.6.0
* :pushpin: Automatic update of dependency boto3 from 1.12.20 to 1.12.21
* :pushpin: Automatic update of dependency pyyaml from 5.3 to 3.13
* :pushpin: Automatic update of dependency boto3 from 1.12.19 to 1.12.20
* :pushpin: Automatic update of dependency boto3 from 1.12.18 to 1.12.19
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.14 to 1.3.15
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.13 to 1.3.14
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* :pushpin: Automatic update of dependency click from 7.0 to 7.1.1
* :pushpin: Automatic update of dependency boto3 from 1.12.16 to 1.12.18
* Remove typeshed dev dependency
* :pushpin: Automatic update of dependency boto3 from 1.12.10 to 1.12.11
* :pushpin: Automatic update of dependency boto3 from 1.12.9 to 1.12.10
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* Add conventions and query template
* Add naming conventions docs for queries
* :pushpin: Automatic update of dependency boto3 from 1.12.8 to 1.12.9
* :pushpin: Automatic update of dependency boto3 from 1.12.7 to 1.12.8
* Fix database migration for python_package_version.is_missing

## Release 0.22.5 (2020-03-20T01:14:38)
* Release of version 0.22.4
* :pushpin: Automatic update of dependency alembic from 1.4.1 to 1.4.2

## Release 0.22.6 (2020-03-27T13:51:27)
* Consider also boolean values
* Optimize accessing dict
* Minor correction for package-update-api
* Consider also raw date without datetime in to_dict()
* Explictly cast datetime to a string
* Fix obtaining model attributes in model.to_dict()
* Correct README for graph-backup-job
* :pushpin: Automatic update of dependency thoth-common from 0.12.3 to 0.12.4
* do not set query
* with_entities
* Join
* :pushpin: Automatic update of dependency boto3 from 1.12.29 to 1.12.30
* Small typo
* New alembic version
* Use Text everywhere
* Created query to retrieve adviser runs to be re run
* Modified logic for adviser sync
* Modify schema and logic to sync adviser run
* :pushpin: Automatic update of dependency thoth-common from 0.12.2 to 0.12.3
* :pushpin: Automatic update of dependency pyyaml from 5.3.1 to 3.13
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.28 to 1.12.29
* Move url filter inside if-if statement
* Update storages function to be more versatile and follow conventions
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.1
* Do not delete rows, keep track of present hashes
* :pushpin: Automatic update of dependency boto3 from 1.12.27 to 1.12.28
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* TODO
* :pushpin: Automatic update of dependency boto3 from 1.12.26 to 1.12.27
* Revert "API calls for package-update-consumer"
* :pushpin: Automatic update of dependency boto3 from 1.12.25 to 1.12.26
* Remove print
* Link Adviser Run with Python Package Versio Entity
* Add arguments and doc string to remove hash
* Function to remove missing hash from database
* reorder function arguments
* Remove unnecessary imports
* Update using subquery
* Specify condition for join
* Remove unecessary join
* Index url is in the pythonpackageindex table
* prepend AdviserRun to origin
* join with PythonSoftware not external
* with ... as session
* Add self as postional argument
* Follow API naming conventions
* Only get packages used by most recent advise
* Add distinct modifier for origin
* Add doc strings and remove unnecessary subtransactions
* API calls for package-update-consumer

## Release 0.22.7 (2020-03-30T10:12:52)
* Drop methods tools to gain performance
* :pushpin: Automatic update of dependency boto3 from 1.12.30 to 1.12.31

## Release 0.22.8 (2020-04-27T09:17:40)
* Corrected wrong keys used in solver sync
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* :pushpin: Automatic update of dependency boto3 from 1.12.43 to 1.12.46
* Adjust method name based on review comment
* Adjust commit message
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* Add logic for syncing revsolver result
* Relock to fix sqlalchemy release hashes
* Introduce get_dependents query
* :pushpin: Automatic update of dependency boto3 from 1.12.38 to 1.12.39
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.15 to 1.3.16
* :pushpin: Automatic update of dependency boto3 from 1.12.37 to 1.12.38
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* :pushpin: Automatic update of dependency boto3 from 1.12.36 to 1.12.37
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.4 to 2.8.5
* Fix return value
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.0 to 0.6.1
* :pushpin: Automatic update of dependency boto3 from 1.12.35 to 1.12.36
* Use RHEL 8
* :pushpin: Automatic update of dependency boto3 from 1.12.34 to 1.12.35
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency boto3 from 1.12.33 to 1.12.34
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.12.4 to 0.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.32 to 1.12.33
* :pushpin: Automatic update of dependency boto3 from 1.12.31 to 1.12.32
* add assignments to query

## Release 0.22.9 (2020-04-27T20:48:26)
* Map ubi to rhel

## Release 0.22.10 (2020-05-13T14:19:08)
* Add correct docstring
* Add query to count a table
* :pushpin: Automatic update of dependency boto3 from 1.13.5 to 1.13.6
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic update of dependency boto3 from 1.13.4 to 1.13.5
* :pushpin: Automatic update of dependency boto3 from 1.13.3 to 1.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.2 to 1.13.3
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency boto3 from 1.12.47 to 1.12.49

## Release 0.22.11 (2020-05-21T22:02:23)
* :pushpin: Automatic update of dependency boto3 from 1.13.14 to 1.13.15
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.13 to 1.13.14
* :pushpin: Automatic update of dependency boto3 from 1.13.12 to 1.13.13
* :pushpin: Automatic update of dependency boto3 from 1.13.11 to 1.13.12
* Add is_missing optional argument to all pypackageversion queries
* Added is_active column
* fixed typo and changed migrations
* Alembic file
* App columns not nullable
* Raise NotFoundError if setting is_missing flag for non-existing package
* :pushpin: Automatic update of dependency boto3 from 1.13.10 to 1.13.11
* docstring match variable name
* pytest failing due to hash mismatch
* Removed table constraints
* Changed order
* add new calling convention for flags/statements
* Updated alembic version
* function for checking current availability of package
* Added kebhut table to models
* :pushpin: Automatic update of dependency boto3 from 1.13.6 to 1.13.9
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.16 to 1.3.17

## Release 0.22.12 (2020-05-28T18:31:30)
* :pushpin: Automatic update of dependency boto3 from 1.13.17 to 1.13.18
* Changed function name
* removed is
* Added method to count active installations
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency boto3 from 1.13.16 to 1.13.17
* add is_missing flag to depends on query
* Fix typo
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.5 to 0.36.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency boto3 from 1.13.15 to 1.13.16
* fixed re-active
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* Added update to readme
* Docstring update
* Added activate deactivate functions

## Release 0.23.0 (2020-06-09T13:14:39)
* Add routines and index for platform manipulation
* Add platform to the schema
* :pushpin: Automatic update of dependency boto3 from 1.13.23 to 1.13.24
* :pushpin: Automatic update of dependency boto3 from 1.13.22 to 1.13.23
* Perform schema version check only if the database is created
* :pushpin: Automatic update of dependency boto3 from 1.13.21 to 1.13.22
* :pushpin: Automatic update of dependency boto3 from 1.13.20 to 1.13.21
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* :pushpin: Automatic update of dependency boto3 from 1.13.19 to 1.13.20
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency boto3 from 1.13.18 to 1.13.19
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* Release of version 0.22.12
* :pushpin: Automatic update of dependency boto3 from 1.13.17 to 1.13.18
* Changed function name
* removed is
* Added method to count active installations
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency boto3 from 1.13.16 to 1.13.17
* add is_missing flag to depends on query
* Fix typo
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.5 to 0.36.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency boto3 from 1.13.15 to 1.13.16
* fixed re-active
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5

## Release 0.23.1 (2020-06-11T20:35:32)
* Change class names and add them to __init__
* break security indicators into two stores
* Release of version 0.23.0
* Add routines and index for platform manipulation
* Add platform to the schema
* :pushpin: Automatic update of dependency boto3 from 1.13.23 to 1.13.24
* :pushpin: Automatic update of dependency boto3 from 1.13.22 to 1.13.23
* create class for storing security indicators
* Perform schema version check only if the database is created
* :pushpin: Automatic update of dependency boto3 from 1.13.21 to 1.13.22
* :pushpin: Automatic update of dependency boto3 from 1.13.20 to 1.13.21
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* :pushpin: Automatic update of dependency boto3 from 1.13.19 to 1.13.20
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency boto3 from 1.13.18 to 1.13.19
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* Release of version 0.22.12
* :pushpin: Automatic update of dependency boto3 from 1.13.17 to 1.13.18
* Changed function name
* removed is
* Added method to count active installations
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency boto3 from 1.13.16 to 1.13.17
* add is_missing flag to depends on query
* Fix typo
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.5 to 0.36.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency boto3 from 1.13.15 to 1.13.16
* fixed re-active


## Release 0.23.2 (2020-06-18T17:24:14)
* Fix migration creating indexes
* Update lock file to fix issues in CI
* :pushpin: Automatic update of dependency boto3 from 1.13.24 to 1.14.1
* Release of version 0.23.1
* Change class names and add them to __init__
* break security indicators into two stores
* Release of version 0.23.0
* Add routines and index for platform manipulation
* Add platform to the schema
* :pushpin: Automatic update of dependency boto3 from 1.13.23 to 1.13.24
* :pushpin: Automatic update of dependency boto3 from 1.13.22 to 1.13.23
* create class for storing security indicators
* Perform schema version check only if the database is created
* :pushpin: Automatic update of dependency boto3 from 1.13.21 to 1.13.22
* :pushpin: Automatic update of dependency boto3 from 1.13.20 to 1.13.21
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* :pushpin: Automatic update of dependency boto3 from 1.13.19 to 1.13.20
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency boto3 from 1.13.18 to 1.13.19
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* Release of version 0.22.12
* :pushpin: Automatic update of dependency boto3 from 1.13.17 to 1.13.18
* Changed function name
* removed is
* Added method to count active installations
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency boto3 from 1.13.16 to 1.13.17
* add is_missing flag to depends on query
* Fix typo
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.5 to 0.36.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency boto3 from 1.13.15 to 1.13.16
* fixed re-active
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* Release of version 0.22.11
* :pushpin: Automatic update of dependency boto3 from 1.13.14 to 1.13.15
* Added update to readme
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.13 to 1.13.14
* Docstring update
* :pushpin: Automatic update of dependency boto3 from 1.13.12 to 1.13.13
* Added activate deactivate functions
* :pushpin: Automatic update of dependency boto3 from 1.13.11 to 1.13.12
* Add is_missing optional argument to all pypackageversion queries
* Added is_active column
* fixed typo and changed migrations
* Alembic file
* App columns not nullable
* Raise NotFoundError if setting is_missing flag for non-existing package
* :pushpin: Automatic update of dependency boto3 from 1.13.10 to 1.13.11
* docstring match variable name
* pytest failing due to hash mismatch
* Removed table constraints
* Changed order
* add new calling convention for flags/statements
* Updated alembic version
* function for checking current availability of package
* Added kebhut table to models
* :pushpin: Automatic update of dependency boto3 from 1.13.6 to 1.13.9
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.16 to 1.3.17
* Release of version 0.22.10
* Add correct docstring
* Add query to count a table
* :pushpin: Automatic update of dependency boto3 from 1.13.5 to 1.13.6
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic update of dependency boto3 from 1.13.4 to 1.13.5
* :pushpin: Automatic update of dependency boto3 from 1.13.3 to 1.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.2 to 1.13.3
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency boto3 from 1.12.47 to 1.12.49
* :pushpin: Automatic update of dependency click from 7.1.1 to 7.1.2
* :pushpin: Automatic update of dependency boto3 from 1.12.46 to 1.12.47
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* Release of version 0.22.9
* Map ubi to rhel
* Release of version 0.22.8
* Corrected wrong keys used in solver sync
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* :pushpin: Automatic update of dependency boto3 from 1.12.43 to 1.12.46
* Adjust method name based on review comment
* Adjust commit message
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* Add logic for syncing revsolver result
* Relock to fix sqlalchemy release hashes
* Introduce get_dependents query
* :pushpin: Automatic update of dependency boto3 from 1.12.38 to 1.12.39
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.15 to 1.3.16
* :pushpin: Automatic update of dependency boto3 from 1.12.37 to 1.12.38
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* :pushpin: Automatic update of dependency boto3 from 1.12.36 to 1.12.37
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.4 to 2.8.5
* Fix return value
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.0 to 0.6.1
* :pushpin: Automatic update of dependency boto3 from 1.12.35 to 1.12.36
* Use RHEL 8
* :pushpin: Automatic update of dependency boto3 from 1.12.34 to 1.12.35
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency boto3 from 1.12.33 to 1.12.34
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.12.4 to 0.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.32 to 1.12.33
* :pushpin: Automatic update of dependency boto3 from 1.12.31 to 1.12.32
* Release of version 0.22.7
* Drop methods tools to gain performance
* :pushpin: Automatic update of dependency boto3 from 1.12.30 to 1.12.31
* add assignments to query
* Release of version 0.22.6
* Consider also boolean values
* Optimize accessing dict
* Minor correction for package-update-api
* Consider also raw date without datetime in to_dict()
* Explictly cast datetime to a string
* Fix obtaining model attributes in model.to_dict()
* Correct README for graph-backup-job
* :pushpin: Automatic update of dependency thoth-common from 0.12.3 to 0.12.4
* do not set query
* with_entities
* Join
* :pushpin: Automatic update of dependency boto3 from 1.12.29 to 1.12.30
* Small typo
* New alembic version
* Use Text everywhere
* Created query to retrieve adviser runs to be re run
* Modified logic for adviser sync
* Modify schema and logic to sync adviser run
* :pushpin: Automatic update of dependency thoth-common from 0.12.2 to 0.12.3
* :pushpin: Automatic update of dependency pyyaml from 5.3.1 to 3.13
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.28 to 1.12.29
* Move url filter inside if-if statement
* Update storages function to be more versatile and follow conventions
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.1
* Do not delete rows, keep track of present hashes
* :pushpin: Automatic update of dependency boto3 from 1.12.27 to 1.12.28
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* TODO
* :pushpin: Automatic update of dependency boto3 from 1.12.26 to 1.12.27
* Revert "API calls for package-update-consumer"
* :pushpin: Automatic update of dependency boto3 from 1.12.25 to 1.12.26
* Remove print
* Link Adviser Run with Python Package Versio Entity
* Release of version 0.22.5
* Release of version 0.22.4
* :pushpin: Automatic update of dependency alembic from 1.4.1 to 1.4.2
* :pushpin: Automatic update of dependency boto3 from 1.12.24 to 1.12.25
* Reduce number of queries for environment markers by caching results
* Add arguments and doc string to remove hash
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* :pushpin: Automatic update of dependency boto3 from 1.12.23 to 1.12.24
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.2 to 0.36.3
* :pushpin: Automatic update of dependency boto3 from 1.12.22 to 1.12.23
* upcase
* Add empty env template
* :pushpin: Automatic update of dependency boto3 from 1.12.21 to 1.12.22
* :pushpin: Automatic update of dependency pytest from 5.3.5 to 5.4.1
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.1 to 0.36.2
* :pushpin: Automatic update of dependency pytest-mypy from 0.5.0 to 0.6.0
* :pushpin: Automatic update of dependency boto3 from 1.12.20 to 1.12.21
* :pushpin: Automatic update of dependency pyyaml from 5.3 to 3.13
* :pushpin: Automatic update of dependency boto3 from 1.12.19 to 1.12.20
* :pushpin: Automatic update of dependency boto3 from 1.12.18 to 1.12.19
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.14 to 1.3.15
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.13 to 1.3.14
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* :pushpin: Automatic update of dependency click from 7.0 to 7.1.1
* :pushpin: Automatic update of dependency boto3 from 1.12.16 to 1.12.18
* Function to remove missing hash from database
* reorder function arguments
* Remove typeshed dev dependency
* Remove unnecessary imports
* Update using subquery
* :pushpin: Automatic update of dependency boto3 from 1.12.10 to 1.12.11
* :pushpin: Automatic update of dependency boto3 from 1.12.9 to 1.12.10
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* Add conventions and query template
* Add naming conventions docs for queries
* :pushpin: Automatic update of dependency boto3 from 1.12.8 to 1.12.9
* Specify condition for join
* Remove unecessary join
* Index url is in the pythonpackageindex table
* prepend AdviserRun to origin
* join with PythonSoftware not external
* with ... as session
* Add self as postional argument
* :pushpin: Automatic update of dependency boto3 from 1.12.7 to 1.12.8
* Follow API naming conventions
* Fix database migration for python_package_version.is_missing
* Release of version 0.22.3
* :pushpin: Automatic update of dependency boto3 from 1.12.6 to 1.12.7
* Only get packages used by most recent advise
* :pushpin: Automatic update of dependency amun from 0.4.0 to 0.4.3
* Move import to local use
* :pushpin: Automatic update of dependency boto3 from 1.12.5 to 1.12.6
* Add distinct modifier for origin
* Add doc strings and remove unnecessary subtransactions
* API calls for package-update-consumer
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.2 to 0.5.0
* :pushpin: Automatic update of dependency boto3 from 1.12.4 to 1.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.3 to 1.12.4
* :pushpin: Automatic update of dependency boto3 from 1.12.2 to 1.12.3
* Alembic update
* flag for missing package version
* :pushpin: Automatic update of dependency amun from 0.3.8 to 0.4.0
* :pushpin: Automatic update of dependency boto3 from 1.12.1 to 1.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.0 to 1.12.1
* Python must have major and minor version
* Change regex expression
* :pushpin: Automatic update of dependency boto3 from 1.11.17 to 1.12.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency boto3 from 1.11.16 to 1.11.17
* Release of version 0.22.2
* :pushpin: Automatic update of dependency boto3 from 1.11.15 to 1.11.16
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* Release of version 0.22.1
* All counts optional
* Add check in sync when report is not provided by Adviser
* :pushpin: Automatic update of dependency boto3 from 1.11.14 to 1.11.15
* Include models using `fullmatch` instead of `search`
* Added option to exclude models from generated schema
* :pushpin: Automatic update of dependency boto3 from 1.11.13 to 1.11.14
* Update .thoth.yaml
* Release of version 0.22.0
* :pushpin: Automatic update of dependency boto3 from 1.11.12 to 1.11.13
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency boto3 from 1.11.11 to 1.11.12
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic update of dependency boto3 from 1.11.10 to 1.11.11
* raise valueError
* Address issue #1573
* Sync missing packages if adviser failed due to unknown dependencies
* Avoid one join in the query
* Fix package symbols query
* Set default to False to reduce logging
* Fix inspection syncing for RHEL
* Fix index creation for symbols queries
* Fix OS name synced in container image analysis
* No need to query for package extract run - software environment can be directly used
* :pushpin: Automatic update of dependency alembic from 1.3.3 to 1.4.0
* :pushpin: Automatic update of dependency boto3 from 1.11.9 to 1.11.10
* normalize, distinct, fix index
* Alembic update
* Change from externalsoftware environment, and uncouple id index
* Move cache to storage level
* Add indexes to improve abi queries
* Filter early
* outer join causing none values
* Refactor query for retrieving symbols in an image
* Make cuda version optional
* Simplified API functions
* Created query to monitor bloat data
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* Fix reference to variable
* Fix method call to serialize models
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* Fixed missing index issue
* :pushpin: Automatic update of dependency amun from 0.3.7 to 0.3.8
* :pushpin: Automatic update of dependency amun from 0.3.6 to 0.3.7
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency amun from 0.3.5 to 0.3.6
* Release of version 0.21.11
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* Add missing keys to inspection schema validation
* :pushpin: Automatic update of dependency boto3 from 1.11.8 to 1.11.9
* :pushpin: Automatic update of dependency boto3 from 1.11.7 to 1.11.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.12 to 1.3.13
* :pushpin: Automatic update of dependency alembic from 1.3.2 to 1.3.3
* new GitHub templates
* added some files to gitignore
* :pushpin: Automatic update of dependency boto3 from 1.11.6 to 1.11.7
* :pushpin: Automatic update of dependency amun from 0.3.4 to 0.3.5
* Added build log analysis result observations to graph database
* Release of version 0.21.10
* Make keys Optional
* :pushpin: Automatic update of dependency amun from 0.3.3 to 0.3.4
* Release of version 0.21.9
* Release of version 0.21.8
* :pushpin: Automatic update of dependency boto3 from 1.11.5 to 1.11.6
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* Adjust parameter in query for PI
* Correct datatype
* Add missing key to sync inspections
* Set Packages Extract flag is_external to True always
* Missing change in query name to follow created standards
* :pushpin: Automatic update of dependency boto3 from 1.11.4 to 1.11.5
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency amun from 0.3.2 to 0.3.3
* Normalize OS version by discarding any minor release in RHEL release string
* :pushpin: Automatic update of dependency boto3 from 1.11.3 to 1.11.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.28
* :sweat_smile: Auto pip and black formatting
* :pushpin: Automatic update of dependency amun from 0.3.1 to 0.3.2
* :pushpin: Automatic update of dependency boto3 from 1.11.2 to 1.11.3
* Release of version 0.21.7
* Introduce a way to parametrize memory cache size
* Create index for has_artifact table
* :pushpin: Automatic update of dependency boto3 from 1.11.1 to 1.11.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* Add index for solved table - it optimizes the has_solver_error query in adviser
* Adjust index for PPV combinations
* Release of version 0.21.6
* :pushpin: Automatic update of dependency boto3 from 1.11.0 to 1.11.1
* Fix query for enabled index
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* Release of version 0.21.5
* :pushpin: Automatic update of dependency amun from 0.3.0 to 0.3.1
* Alembic didn't create correct change in schema
* Release of version 0.21.4
* Consider only enabled indexes in unsolved queries
* Query for index_url before creating index
* Introduce a query for retrieving Python package entity names
* :pushpin: Automatic update of dependency boto3 from 1.10.50 to 1.11.0
* Release of version 0.21.3
* Adjust datatype for conv PI to sync inspection results
* Release of version 0.21.2
* Release of version 0.21.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* Fix parameter name for syncing provenance-checker documents
* Provide environment variable marker flag when retrieving transitive deps
* Adjust syncing logic of Dependency Monkey documents based on the current output
* Correct inspection sync key
* :pushpin: Automatic update of dependency amun from 0.2.7 to 0.3.0
* Release of version 0.21.0
* :pushpin: Automatic update of dependency boto3 from 1.10.49 to 1.10.50
* :pushpin: Automatic update of dependency thoth-python from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency boto3 from 1.10.48 to 1.10.49
* Use datetime to sort results
* Do not use id when counting tables
* Fix advised software stack sync
* :pushpin: Automatic update of dependency thoth-python from 0.8.0 to 0.9.0
* Format using black
* Drop id columns on relation tables
* Create index for CVE step to omit sequence scan
* :pushpin: Automatic update of dependency boto3 from 1.10.47 to 1.10.48
* Release of version 0.20.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* Fix syncing external software environments coming from adviser
* Release of version 0.20.5
* :pushpin: Automatic update of dependency thoth-python from 0.7.1 to 0.8.0
* Adjust model performance for inspection output
* Correct key from inspection output
* correct typo
* Missing randomize
* Adjust to follow naming convention
* Introduce software environment specific queries
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.3 to 1.3.4
* :pushpin: Automatic update of dependency pyyaml from 5.2 to 5.3
* :pushpin: Automatic update of dependency boto3 from 1.10.46 to 1.10.47
* Release of version 0.20.4
* Fix wrong argument name propagated
* Release of version 0.20.3
* Fix syncs in versions
* Release of version 0.20.2
* Happy new year!
* Remove string size limitations from depends_on table
* Release of version 0.20.1
* :sparkles: added a PR template
* Fix keyword argument passing
* :pushpin: Automatic update of dependency boto3 from 1.10.45 to 1.10.46
* Release of version 0.20.0
* Sync package version requested rather than package version reported
* Optimize marker evaluation result query for adviser
* :pushpin: Automatic update of dependency boto3 from 1.10.44 to 1.10.45
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.0 to 0.36.1
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency boto3 from 1.10.43 to 1.10.44
* Do not show alembic info on configure_logger
* :pushpin: Automatic update of dependency boto3 from 1.10.42 to 1.10.43
* Super has no __del__
* Do not dispose engine in destructor
* Log number of dumps maintained
* Adjust names of parameters to respect their semantics
* Implement rotation of backups
* Fixes in reStructuredText in README file
* :pushpin: Automatic update of dependency boto3 from 1.10.41 to 1.10.42
* :pushpin: Automatic update of dependency boto3 from 1.10.40 to 1.10.41
* Release of version 0.19.30
* Release of version 0.19.29
* Increment solver error cache
* :pushpin: Automatic update of dependency alembic from 1.3.1 to 1.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.39 to 1.10.40
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.11 to 1.3.12
* Increase cache for caching solver errors
* Introduce PyBench PI table and adjust sync logic for inspection
* Remove unused indexes in depends_on table
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.38 to 1.10.39
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency boto3 from 1.10.35 to 1.10.38
* Fix Automatic Update Failure
* Sync cuda version
* Add missing filter
* :pushpin: Automatic update of dependency boto3 from 1.10.34 to 1.10.35
* Release of version 0.19.28
* Generalize function to retrieve multi values key metadata
* Add platforms
* WIP: Adjust Python Package Metadata query
* Add Thamos documentation
* Document automatic graph-backup job
* More formatting changes
* Minor docs reformatting
* Show database schema
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.35.0 to 0.36.0
* Provide is_s2i flag for adviser runs
* Point documentation to other libraries
* Add aggregated_at column to CVE
* Select distinct CVEs
* Remove duplicate entry
* Adjust tests to new metadata
* Add deployment name to the result schema
* Release of version 0.19.27
* UBI:8 has optional variant_id
* :pushpin: Automatic update of dependency boto3 from 1.10.33 to 1.10.34
* Release of version 0.19.26
* Add Google Analytics
* Adjust testsuite
* Provide OS release schema
* Adjust default is_provided value
* Rename flag to is_provided_package_version
* Change Sphinx theme
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency boto3 from 1.10.32 to 1.10.33
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* :pushpin: Automatic update of dependency boto3 from 1.10.31 to 1.10.32
* :pushpin: Automatic update of dependency boto3 from 1.10.30 to 1.10.31
* Make some log info optional
* Correct staticmethod
* :pushpin: Automatic update of dependency boto3 from 1.10.29 to 1.10.30
* :pushpin: Automatic update of dependency pyyaml from 5.1.2 to 5.2
* :pushpin: Automatic update of dependency boto3 from 1.10.28 to 1.10.29
* Create index for get_depends_on query
* Do not sync package errors if the given package is not provided
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.19
* Release of version 0.19.25
* Adjust tests to the new implementation
* Increase characters metadata in keywords and summary metadata
* Optimized Solved quries with error
* Optimize Analyzed Python Packages queries
* Optimnize unsolved queries
* Optimize queries
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* Cache environment marker evaluation result
* :package: store database backup to ceph storage
* Fix Issue #1308 not iterable
* Fix alembic configuration instantiation issues
* Gather document id from document_id field
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* Use open instead of pathlib to adress PV in-cluster issues
* :pushpin: Automatic update of dependency boto3 from 1.10.26 to 1.10.27
* Make library thread safe
* Issue warning instead of error
* Introduced sorting type in queries
* :pushpin: Automatic update of dependency sqlalchemy-stubs from 0.2 to 0.3
* Fix wrong staticmethod
* :pushpin: Automatic update of dependency boto3 from 1.10.25 to 1.10.26
* Release of version 0.19.24
* Fix referencing store if is_local is set
* Add ability to sync documents based on absolute path
* :pushpin: Automatic update of dependency boto3 from 1.10.24 to 1.10.25
* :pushpin: Automatic update of dependency boto3 from 1.10.23 to 1.10.24
* Release of version 0.19.23
* Remove self to make method static
* Use context manager for handling sessions
* :pushpin: Automatic update of dependency boto3 from 1.10.22 to 1.10.23
* :pushpin: Automatic update of dependency boto3 from 1.10.21 to 1.10.22
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.20 to 1.10.21
* :pushpin: Automatic update of dependency boto3 from 1.10.19 to 1.10.20
* Fix warning for migration configuration check
* Release of version 0.19.22
* Correct output of queries
* Release of version 0.19.21
* Use same version as in the cluster
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* :pushpin: Automatic update of dependency boto3 from 1.10.18 to 1.10.19
* Fix wrong rebase
* Dispose engine on disconnect
* Dispose engine on connect issues
* Release of version 0.19.20
* Use default pooling from sqlalchemy
* Adjust output query for metric
* Introduce ping method
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency boto3 from 1.10.17 to 1.10.18
* Optimized/Improved query to retrieve unsolved Python Packages
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* Fix schema check
* :pushpin: Automatic update of dependency boto3 from 1.10.16 to 1.10.17
* State ignoring a role assignment in docs
* :pushpin: Automatic update of dependency alembic from 1.3.0 to 1.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* Release of version 0.19.19
* :pushpin: Automatic update of dependency boto3 from 1.10.15 to 1.10.16
* Fix wrong propagation of is_local flag
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.10 to 1.3.11
* :pushpin: Automatic update of dependency boto3 from 1.10.14 to 1.10.15
* :green_heart: added more builds that need to be triggered
* Increase character length for keywords metadata
* :pushpin: Automatic update of dependency boto3 from 1.10.13 to 1.10.14
* Release of version 0.19.18
* Correct attribute for metadata Provides-Extra
* Fix bug in checking for dist key
* :pushpin: Automatic update of dependency thoth-python from 0.6.5 to 0.7.1
* :pushpin: Automatic update of dependency boto3 from 1.10.12 to 1.10.13
* Release of version 0.19.17
* Adjust sync for inspections
* Standardize sync logic entries for Adviser, Provenance Checker and Dependency Monkey
* :pushpin: Automatic update of dependency boto3 from 1.10.11 to 1.10.12
* :pushpin: Automatic update of dependency boto3 from 1.10.10 to 1.10.11
* Minor changes
* Added MetadataDistutils, updated sync logic, schema docs, Tested syncs
* Release of version 0.19.16
* :pushpin: Automatic update of dependency boto3 from 1.10.9 to 1.10.10
* Pick metadata which were computed
* Grouped Metadata Distutils
* Created MetadataProvidesExtra
* Created MetadataProjectUrl
* Created MetadataRequiresExternal
* Created MetadataRequiresDist and MetadataSupportedPlatform
* Created MetadataPlatform
* New models for PythonPackage Metadata that have multiple values
* Cache some of the query results
* :pushpin: Automatic update of dependency python-dateutil from 2.8.1 to 2.8.0
* :pushpin: Automatic update of dependency boto3 from 1.10.8 to 1.10.9
* Fix query to CVE for a given python package version entity
* Graph database cache has been removed
* Sync documents from a local directory if requested
* Release of version 0.19.15
* Relax fatal error on syncing unmatched metadata
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.1 to 0.4.2
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* Randomize retrievals of unanalyzed Python packages
* Randomize retrieval of unsolved Python packages
* Remove old pydgraph dependency
* :pushpin: Automatic update of dependency boto3 from 1.10.7 to 1.10.8
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.34.2 to 0.35.0
* :pushpin: Automatic update of dependency boto3 from 1.10.6 to 1.10.7
* :pushpin: Automatic update of dependency alembic from 1.2.1 to 1.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.5 to 1.10.6
* Correct errors for pytest
* Introduce enum classes for safe API
* Turn off checking thoth module by mypy
* Start using mypy in strict mode
* Fix retrieval of Python digests query
* :pushpin: Automatic update of dependency boto3 from 1.10.4 to 1.10.5
* Release of version 0.19.14
* Fix model for index url in the query
* Keep Python package tuples positional arguments
* Issue warning if the database schema is not initialized yet in connect
* Add normalization for package_name and package_version
* Standardize and unify query for python artifact hashes
* Release of version 0.19.13
* Update naming queries according to Thoth convention
* State maintainer and project url in setup.py
* Issue warning on connection to the database if schema is not up2date
* Update the schema
* Sync container image size
* :pushpin: Automatic update of dependency boto3 from 1.10.3 to 1.10.4
* :pushpin: Automatic update of dependency boto3 from 1.10.2 to 1.10.3
* Query to retrieve ML frameworks names
* Correct query to get metadata for Python Package
* HasArtifact is linked with PythonPackageVersionEntity table
* Revert "Symbol-API"
* Drop unique constraint in depends_on table
* added the registry to look for pgweb
* added podman-compose to dev packages list
* :pushpin: Automatic update of dependency methodtools from 0.1.1 to 0.1.2
* Fix model assignment when syncing results of Python interpreters
* Release of version 0.19.12
* Fixing the func argunment names
* Fixing the func argunment design
* consistency in using the variable force
* Fix index url issue, now properly
* Fix index_url key, now properly
* Fix version key dereference
* Fix index url key in new solvers implementation
* Release of version 0.19.11
* :pushpin: Automatic update of dependency pytest from 5.2.1 to 5.2.2
* :pushpin: Automatic update of dependency boto3 from 1.10.1 to 1.10.2
* :pushpin: Automatic update of dependency methodtools from 0.1.0 to 0.1.1
* :pushpin: Automatic update of dependency boto3 from 1.10.0 to 1.10.1
* Handle issues in a better way
* Increase lines per file in Coala configuration
* Query environment markers stored in the database
* Introduce query for checking marker evaluation results
* Add support for extras in the Python package dependencies retrieval query
* Remove graph cache tests
* Introduce additional exception types for specific exceptions raised
* Drop cache support
* Updated .coafile to allow for longer files
* Coala errors
* More verbose errors, require all parameters
* :pushpin: Automatic update of dependency boto3 from 1.9.253 to 1.10.0
* Add offset and count
* Increase max lines per file
* Add api to get versioned symbols
* Get internal software & hardware environments
* Start using mypy for type checks
* Add missing provides-extra column to Python metadata
* Add missing columns to Python metadata
* :pushpin: Automatic update of dependency thoth-python from 0.6.4 to 0.6.5
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.3 to 2.8.4
* :pushpin: Automatic update of dependency boto3 from 1.9.252 to 1.9.253
* Generic webhook updated to trigger the build from zuul
* Release of version 0.19.10
* Add update sync schema for PackageExtract
* Correct syncing issue
* Allow nullable software environemnts in the schema
* Fix multiple heads present
* Fix reference to variable in the query
* Fix signature of the private method - unsolved edge cases
* Fix query to retrieve number of unsolved packages
* Fix error when case 3 is not declared yet
* Created query for python package metadata for user-api
* Created and updated queries for analyzed packages
* :pushpin: Automatic update of dependency boto3 from 1.9.251 to 1.9.252
* :pushpin: Automatic update of dependency boto3 from 1.9.250 to 1.9.251
* Sync python interpreters
* :pushpin: Automatic update of dependency boto3 from 1.9.249 to 1.9.250
* New schema and sync in Solver for PythonPackageMetadata
* :pushpin: Automatic update of dependency boto3 from 1.9.248 to 1.9.249
* :pushpin: Automatic update of dependency boto3 from 1.9.247 to 1.9.248
* Queries for packages with error in solvers and adjust schema
* Increase lenght file
* :pushpin: Automatic update of dependency boto3 from 1.9.246 to 1.9.247
* Consistenly sync index_url and package_version
* Added dependency monkey schema
* Added schema for package extract
* Added schema for package-extract sync
* Added solver sync schema
* Fix linkage of artifacts in Python package version entities
* Created adviser sync schema
* Add thoth sync schema for Amun
* Added provenance checker sync and all components sync
* Created docs for syncs inside Thoth Database
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.3 to 0.6.4
* Queries for packages with error in solvers and adjust schema
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.9 to 1.3.10
* :pushpin: Automatic update of dependency boto3 from 1.9.245 to 1.9.246
* Updated and tested all solved/unsolved functions
* Created solver functions following  naming convention
* :pushpin: Automatic update of dependency boto3 from 1.9.244 to 1.9.245
* Add missing import
* Remove unused import
* Created is_external for PackageExtractRun
* Remove old file for Dgraph related tests
* State how to implement syncing logic for any workload job done in the cluster
* Raise not found error if the given Python index is not found
* :pushpin: Automatic update of dependency boto3 from 1.9.243 to 1.9.244
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* Update syncs
* Changed schema and Added new Tables
* Fix performance indicator name
* :pushpin: Automatic update of dependency pytest from 5.2.0 to 5.2.1
* :pushpin: Automatic update of dependency pytest-cov from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency boto3 from 1.9.242 to 1.9.243
* Update functions for metrics
* :pushpin: Automatic update of dependency pytest-cov from 2.7.1 to 2.8.0
* Add examples to docstrings
* :pushpin: Automatic update of dependency boto3 from 1.9.241 to 1.9.242
* Generate migration for new schema
* Add logic for syncing marker and extra
* :pushpin: Automatic update of dependency boto3 from 1.9.240 to 1.9.241
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* Convert function according to new naming convention
* Remove obsolete exception
* Expose sync_documents outside of module
* Minor fix to address typo
* Implement a generic approach to sync any document
* :pushpin: Automatic update of dependency boto3 from 1.9.239 to 1.9.240
* Sync duration
* Generalized module varibale for count
* Created functions for get_python_packages cases
* Correct outputs
* New python_package_versions_count functions
* Hide query
* Added distinct flag
* No NULL values for some PythonPackageVersion attributes
* New query
* get_python_package_version_count
* :pushpin: Automatic update of dependency boto3 from 1.9.238 to 1.9.239
* New queries for python packages
* Release of version 0.19.9
* Fix testsuite with recent changes
* :pushpin: Automatic update of dependency pytest from 5.1.3 to 5.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.237 to 1.9.238
* Add duration to the result schema
* Release of version 0.19.8
* New query: count software stacks per type
* :pushpin: Automatic update of dependency boto3 from 1.9.236 to 1.9.237
* New queries
* Update queries
* We use psql not pg_restore
* Show an example run how to create a local PostgreSQL instance
* :pushpin: Automatic update of dependency boto3 from 1.9.235 to 1.9.236
* Use podman-compose
* Log what is being synced during graph syncs
* State graphviz package as a dependency when generating schema images
* :pushpin: Automatic update of dependency alembic from 1.2.0 to 1.2.1
* :pushpin: Automatic update of dependency boto3 from 1.9.234 to 1.9.235
* Release of version 0.19.7
* Fix path to alembic versions - it has changed recently
* Allow limit latest versions to be None
* :pushpin: Automatic update of dependency boto3 from 1.9.233 to 1.9.234
* Make solver name optional when retrieving unsolved packages
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* Introduce a check to verify the current database schema is up2date
* Drop also alembic version table
* Distribute alembic migrations with thoth-storages
* Release of version 0.19.6
* Add missing migrations to requirements.txt file
* :pushpin: Automatic update of dependency pytest from 5.1.2 to 5.1.3
* :pushpin: Automatic update of dependency boto3 from 1.9.232 to 1.9.233
* :pushpin: Automatic update of dependency alembic from 1.1.0 to 1.2.0
* Normalize Python package versions before each insert or query
* :pushpin: Automatic update of dependency boto3 from 1.9.231 to 1.9.232
* Fix small typo
* Make sure devs update to most recent version before generating new versions
* Minor typo fixes in README file
* Make coala happy
* Use UTC when generating schema versions
* Generate initial schema using Alembic
* Start using Alembic for database migrations
* Add missing method used to register new packages in package releases
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency boto3 from 1.9.230 to 1.9.231
* Release of version 0.19.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* Document how to dump and restore database in the running cluster
* Adjust logged message to inform about concurrent writes
* Randomize retrieval of unsolved Python packages
* New class methods for InspectionStore
* Fix unsolved Python packages query
* Adjust signature of method to respect its return value
* Release of version 0.19.4
* Count and limit for advises can be nullable
* Increase advisory message for CVEs
* :pushpin: Automatic update of dependency boto3 from 1.9.229 to 1.9.230
* Release of version 0.19.3
* Disable connection pooling
* Release of version 0.19.2
* Update inspection sync for Upsert behaviour
* Fix documentation for performance indicators
* Implemented CASCADE on delete for Foreign Keys
* Release of version 0.19.1
* :pushpin: Automatic update of dependency thoth-python from 0.6.1 to 0.6.2
* Release of version 0.19.0
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
* Use more generic env variable names
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
* Release of version 0.18.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* Provide method for counting number of unsolved Python packages
* Fix query for retrieving unsolved Python packages
* :pushpin: Automatic update of dependency boto3 from 1.9.206 to 1.9.207
* Add models for versioned symbols and associated edges
* Minor changes to the function which returns unanalyzed packages
* Retrieve packages that are not analyzed by Package-Analyzer
* :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* :pushpin: Automatic update of dependency voluptuous from 0.11.5 to 0.11.7
* :pushpin: Automatic update of dependency boto3 from 1.9.205 to 1.9.206
* :pushpin: Automatic update of dependency thoth-python from 0.6.0 to 0.6.1
* Release of version 0.18.5
* Introduce a flag to retrieve only solved packages
* Use Python package name normalization from thoth-python module
* :pushpin: Automatic update of dependency boto3 from 1.9.204 to 1.9.205
* :pushpin: Automatic update of dependency boto3 from 1.9.203 to 1.9.204
* Release of version 0.18.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* :pushpin: Automatic update of dependency boto3 from 1.9.202 to 1.9.203
* Fix Package Analyzer results syncing
* Fixes Syncing of Package Extract results
* :pushpin: Automatic update of dependency boto3 from 1.9.201 to 1.9.202
* :pushpin: Automatic update of dependency boto3 from 1.9.200 to 1.9.201
* Fix key error 'python'
* :pushpin: Automatic update of dependency boto3 from 1.9.199 to 1.9.200
* Release of version 0.18.3
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

## Release 0.24.0 (2020-06-23T20:53:00)
* Add import
* Add database
* make coala happy
* Update .zuul.yaml
* No inspection result batch size
* remove variables
* Reproduce methods specific for postgres
* Use variable only
* remove imports
* Adjust methods
* small change
* remove sqlalchemy utils
* more info
* more messages
* Move imports of amun to local scope
* Introduce a method for checking if the given inspection exists
* Fix computing batch size of inspection jobs
* Add missing exports of inspection adapters
* Remove parts moved to thoth-common

## Release 0.24.1 (2020-07-07T06:56:06)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.6 to 0.36.7 (#1876)
* :pushpin: Automatic update of dependency thoth-common from 0.14.0 to 0.14.1 (#1875)
* :pushpin: Automatic update of dependency boto3 from 1.14.14 to 1.14.17 (#1874)
* Sync si aggregated (#1873)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.0 (#1872)
* Fix missing normalize_os_version (#1868)
* :pushpin: Automatic update of dependency boto3 from 1.14.13 to 1.14.14 (#1866)
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13 (#1865)
* :pushpin: Automatic update of dependency boto3 from 1.14.9 to 1.14.13 (#1864)
* Source type column (#1862)
* Update OWNERS
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.17 to 1.3.18
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Update OWNERS

## Release 0.24.2 (2020-07-08T12:02:05)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.7 to 0.36.8 (#1889)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.7 to 0.36.8 (#1887)
* :pushpin: Automatic update of dependency boto3 from 1.14.17 to 1.14.18 (#1886)

## Release 0.24.3 (2020-07-09T15:17:14)
* Sync inspections results (#1892)
* :pushpin: Automatic update of dependency boto3 from 1.14.18 to 1.14.19 (#1894)
* Do raise on counting, return zero instead (#1893)

## Release 0.24.4 (2020-07-17T07:50:49)
* Default platform if not available in the solver document (#1901)
* :pushpin: Automatic update of dependency pytest-timeout from 1.4.1 to 1.4.2 (#1900)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#1899)
* :pushpin: Automatic update of dependency boto3 from 1.14.19 to 1.14.21 (#1898)
* Map old domain to new (#1897)

## Release 0.24.5 (2020-07-23T15:08:59)
* Use method from thoth-common (#1907)
* :pushpin: Automatic update of dependency boto3 from 1.14.22 to 1.14.26 (#1908)

## Release 0.25.0 (2020-07-30T08:29:14)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0 (#1921)
* :pushpin: Automatic update of dependency boto3 from 1.14.30 to 1.14.31 (#1920)
* adding aggregated points to wrong location (#1919)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.15.0 (#1915)
* :pushpin: Automatic update of dependency boto3 from 1.14.28 to 1.14.30 (#1914)
* :pushpin: Automatic update of dependency boto3 from 1.14.26 to 1.14.28 (#1912)
* Use postgres 10.12 in podman-compose as in the cluster (#1911)

## Release 0.25.1 (2020-08-17T08:20:11)
* :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#1935)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#1934)
* :pushpin: Automatic update of dependency pytest from 6.0.0 to 6.0.1 (#1933)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#1932)
* :pushpin: Automatic update of dependency boto3 from 1.14.31 to 1.14.43 (#1931)
* add cache and return None if empty (#1929)
* Add long_description_content_type (#1927)
* :pushpin: Automatic update of dependency thoth-common from 0.15.0 to 0.16.0 (#1924)

## Release 0.25.2 (2020-08-19T11:42:37)
* :pushpin: Automatic update of dependency boto3 from 1.14.43 to 1.14.45 (#1941)
* Add information about heads on schema up2date check (#1917)
* Add security and performance database enums (#1940)
* Fix revsolver syncing logic (#1944)

## Release 0.25.3 (2020-08-20T18:40:19)
* :pushpin: Automatic update of dependency boto3 from 1.14.45 to 1.14.46 (#1950)
* Fix logging error when database schema is not up2date (#1949)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.18 to 1.3.19 (#1943)

## Release 0.25.4 (2020-08-21T07:31:14)
* Propagate platform information in dependents query (#1954)
* Propagate platform when syncing revsolver results (#1955)
* :pushpin: Automatic update of dependency boto3 from 1.14.46 to 1.14.47 (#1956)

## Release 0.25.5 (2020-08-21T15:30:50)
* Add filters to method

## Release 0.25.6 (2020-08-26T19:30:11)
* query.all returns type List[result] not List[str]

## Release 0.25.7 (2020-09-10T18:35:54)
### Features
* Added query to get SI unanalyzed packages (#1963)
* Introduce query for document ids with solver error (#1976)
* :arrow_up: Relock the pipfile.lock
### Improvements
* Make package version and package index optional in get_depends_on (#1975)
* State how to install podman and podman-compose (#1971)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.18.0 to 0.18.1 (#1983)
* :pushpin: Automatic update of dependency thoth-common from 0.17.3 to 0.18.0 (#1982)
* :pushpin: Automatic update of dependency boto3 from 1.14.57 to 1.14.58 (#1981)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.2 (#1973)
* :pushpin: Automatic update of dependency boto3 from 1.14.49 to 1.14.53 (#1972)
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#1970)
* :pushpin: Automatic update of dependency boto3 from 1.14.47 to 1.14.49 (#1969)

## Release 0.25.8 (2020-09-11T21:39:02)
### Features
* Add queries for SI metrics
### Automatic Updates
* :pushpin: Automatic update of dependency alembic from 1.4.2 to 1.4.3 (#1991)
* :pushpin: Automatic update of dependency alembic from 1.4.2 to 1.4.3 (#1990)
* :pushpin: Automatic update of dependency thoth-common from 0.18.1 to 0.18.2 (#1989)
* :pushpin: Automatic update of dependency boto3 from 1.14.58 to 1.14.60 (#1988)

## Release 0.25.9 (2020-09-15T12:40:57)
### Features
* Remove package-analyzer related bits (#1994)
### Improvements
* Add query for adviser run per source type (#1997)
### Automatic Updates
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#1996)
* :pushpin: Automatic update of dependency thoth-common from 0.18.2 to 0.19.0 (#1999)
* :pushpin: Automatic update of dependency boto3 from 1.14.60 to 1.14.61 (#1998)

## Release 0.25.10 (2020-09-16T14:47:02)
### Features
* Fix sync for security (#2002)

## Release 0.25.11 (2020-09-21T16:04:13)
### Features
* Adjust comment
* Adjust query for SI unanalyzed
* Add query to retrieve packages SI analyzed
* Adjust SI queries after schema change
* Invert order to allow sync (#2010)
### Automatic Updates
* :pushpin: Automatic update of dependency voluptuous from 0.11.7 to 0.12.0 (#2011)
* :pushpin: Automatic update of dependency boto3 from 1.14.63 to 1.15.1 (#2012)
* :pushpin: Automatic update of dependency boto3 from 1.14.62 to 1.14.63 (#2009)
* :pushpin: Automatic update of dependency boto3 from 1.14.61 to 1.14.62 (#2006)

## Release 0.25.12 (2020-09-29T07:44:45)
### Features
* Adjust query for new flag is_downloadable (#2027)
* Correct docstring (#2025)
* add func for updating downloadable function (#2022)
* add flag for missing src distro (#2021)
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.15.6 to 1.15.7 (#2026)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#2023)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#2020)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#2019)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#2018)
* :pushpin: Automatic update of dependency boto3 from 1.15.1 to 1.15.6 (#2017)

## Release 0.25.13 (2020-09-29T09:22:07)
### Features
* Rename flag to be generalized (#2030)

## Release 0.25.14 (2020-09-30T19:19:52)
### Features
* Correct queries after changes in schema (#2036)
* Added changes to kebechet model (#2024)
### Bug Fixes
* Alembic timeline fix (#2035)
### Improvements
* change flag name and alembic commands (#2033)
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.15.7 to 1.15.8 (#2034)

## Release 0.25.15 (2020-10-03T16:31:54)
### Features
* Adjust docstring (#2037)

## Release 0.25.16 (2020-10-30T14:57:14)
### Features
* Adjust query filters (#2065)
* Adjust alembic migration (#2064)
* add error flag to si-sync (#2054)
* Fix cache handling and add ability to drop the cache (#2050)
### Automatic Updates
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#2062)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#2061)
* :pushpin: Automatic update of dependency boto3 from 1.16.6 to 1.16.8 (#2060)
* :pushpin: Automatic update of dependency boto3 from 1.16.0 to 1.16.6 (#2057)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#2056)
* :pushpin: Automatic update of dependency boto3 from 1.15.16 to 1.16.0 (#2055)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#2053)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#2052)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.19 to 1.3.20 (#2051)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1
* :pushpin: Automatic update of dependency boto3 from 1.15.11 to 1.15.16

## Release 0.25.17 (2020-11-04T20:51:27)
### Features
* Match location where provenance-checker documents are stored (#2070)
* :sparkles: ignore more
### Improvements
* :arrow_down: removed the files as they are no longer required
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.16.8 to 1.16.9

## Release 0.26.0 (2020-11-05T12:47:00)
### Features
* Provide a method for storing user requests (#2078)
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.16.10 to 1.16.11 (#2082)
* :pushpin: Automatic update of dependency boto3 from 1.16.10 to 1.16.11 (#2081)
* :pushpin: Automatic update of dependency boto3 from 1.16.9 to 1.16.10 (#2076)

## Release 0.26.1 (2020-11-10T23:33:13)
### Features
* Adjust DM sync (#2086)
### Bug Fixes
* Raise an exception when the given record was not found (#2069)
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.16.11 to 1.16.12 (#2087)

## Release 0.27.0 (2020-11-18T06:35:16)
### Features
* Changes in schema for bug, internal trigger and data analysis (#2046)
### Improvements
* check for cuda nvcc and found in file version (#2092)

## Release 0.27.1 (2020-11-18T10:43:11)
### Features
* Install thoth-ssdeep requirement for thoth-storages

## Release 0.28.0 (2020-11-23T14:53:41)
### Features
* add function to run amcheck and check for db corruption (#2105)

## Release 0.29.0 (2020-11-23T15:04:37)
### Features
* Release of version 0.28.0 (#2112)
* add function to run amcheck and check for db corruption (#2105)
* Release of version 0.27.1 (#2103)
* Install thoth-ssdeep requirement for thoth-storages
* Release of version 0.27.0 (#2100)
* Changes in schema for bug, internal trigger and data analysis (#2046)
* Release of version 0.26.1 (#2090)
* Adjust DM sync (#2086)
* Release of version 0.26.0
* Provide a method for storing user requests (#2078)
* Release of version 0.25.17 (#2077)
* Match location where provenance-checker documents are stored (#2070)
* :sparkles: ignore more
* Release of version 0.25.16 (#2067)
* Adjust query filters (#2065)
* Adjust alembic migration (#2064)
* add error flag to si-sync (#2054)
* Fix cache handling and add ability to drop the cache (#2050)
* Release of version 0.25.15 (#2044)
* Adjust docstring (#2037)
* Release of version 0.25.14
* Correct queries after changes in schema (#2036)
* Added changes to kebechet model (#2024)
* Release of version 0.25.13 (#2032)
* Rename flag to be generalized (#2030)
* Release of version 0.25.12 (#2029)
* Adjust query for new flag is_downloadable (#2027)
* Correct docstring (#2025)
* add func for updating downloadable function (#2022)
* add flag for missing src distro (#2021)
* Release of version 0.25.11 (#2015)
* Adjust comment
* Adjust query for SI unanalyzed
* Add query to retrieve packages SI analyzed
* Adjust SI queries after schema change
* Invert order to allow sync (#2010)
* Release of version 0.25.10 (#2005)
* Fix sync for security (#2002)
* Release of version 0.25.9 (#2001)
* Remove package-analyzer related bits (#1994)
* Release of version 0.25.8 (#1993)
* Add queries for SI metrics
* Release of version 0.25.7 (#1986)
* Added query to get SI unanalyzed packages (#1963)
* Introduce query for document ids with solver error (#1976)
* :arrow_up: Relock the pipfile.lock
* Release of version 0.25.6
* query.all returns type List[result] not List[str]
* Release of version 0.25.5 (#1962)
* Add filters to method
* Release of version 0.25.4 (#1958)
* Propagate platform information in dependents query (#1954)
* Propagate platform when syncing revsolver results (#1955)
* Release of version 0.25.3 (#1953)
* Release of version 0.25.2 (#1946)
* Add information about heads on schema up2date check (#1917)
* Fix revsolver syncing logic (#1944)
* Release of version 0.25.1 (#1938)
* add cache and return None if empty (#1929)
* Add long_description_content_type (#1927)
* Release of version 0.25.0 (#1923)
* adding aggregated points to wrong location (#1919)
* Use postgres 10.12 in podman-compose as in the cluster (#1911)
* Release of version 0.24.5 (#1910)
* Use method from thoth-common (#1907)
* Release of version 0.24.4 (#1904)
* Map old domain to new (#1897)
* Release of version 0.24.3 (#1896)
* Sync inspections results (#1892)
* Do raise on counting, return zero instead (#1893)
* Release of version 0.24.2 (#1891)
* Release of version 0.24.1 (#1878)
* Adjust SI classes (#1881)
* Remove plural, only one build is done per inspection (#1880)
* Sync si aggregated (#1873)
* Fix missing normalize_os_version (#1868)
* Source type column (#1862)
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Release of version 0.24.0
* Add import
* Add database
* Update .zuul.yaml
* Use variable only
* small change
* more messages
* Move imports of amun to local scope
* Introduce a method for checking if the given inspection exists
* Add missing exports of inspection adapters
* Implement adapters for inspections
* Maintain order
* Release of version 0.23.2
* Add import or classes cannot be accessed
* Remove parts moved to thoth-common
* Fix migration creating indexes
* Release of version 0.23.1
* Change class names and add them to __init__
* Release of version 0.23.0
* Add platform to the schema
* Perform schema version check only if the database is created
* added a 'tekton trigger tag_release pipeline issue'
* Release of version 0.22.12
* Changed function name
* removed is
* Added method to count active installations
* add is_missing flag to depends on query
* Release of version 0.22.11
* Added update to readme
* Docstring update
* Added activate deactivate functions
* Add is_missing optional argument to all pypackageversion queries
* Added is_active column
* Alembic file
* App columns not nullable
* Removed table constraints
* Changed order
* add new calling convention for flags/statements
* Updated alembic version
* Added kebhut table to models
* Release of version 0.22.10
* Add correct docstring
* Add query to count a table
* :pushpin: Automatic dependency re-locking
* Release of version 0.22.9
* Map ubi to rhel
* Release of version 0.22.8
* Adjust commit message
* Introduce get_dependents query
* Fix return value
* Use RHEL 8
* Release of version 0.22.7
* add assignments to query
* Release of version 0.22.6
* Consider also boolean values
* Optimize accessing dict
* Minor correction for package-update-api
* Consider also raw date without datetime in to_dict()
* Explictly cast datetime to a string
* Fix obtaining model attributes in model.to_dict()
* Correct README for graph-backup-job
* do not set query
* with_entities
* Join
* New alembic version
* Use Text everywhere
* Created query to retrieve adviser runs to be re run
* Move url filter inside if-if statement
* Do not delete rows, keep track of present hashes
* TODO
* Revert "API calls for package-update-consumer"
* Remove print
* Link Adviser Run with Python Package Versio Entity
* Release of version 0.22.5
* Release of version 0.22.4
* Reduce number of queries for environment markers by caching results
* Add arguments and doc string to remove hash
* upcase
* Add empty env template
* Function to remove missing hash from database
* reorder function arguments
* Remove typeshed dev dependency
* Update using subquery
* Add conventions and query template
* Add naming conventions docs for queries
* Specify condition for join
* Remove unecessary join
* Index url is in the pythonpackageindex table
* prepend AdviserRun to origin
* with ... as session
* Add self as postional argument
* Follow API naming conventions
* Fix database migration for python_package_version.is_missing
* Release of version 0.22.3
* Only get packages used by most recent advise
* Move import to local use
* Add distinct modifier for origin
* API calls for package-update-consumer
* Alembic update
* flag for missing package version
* Change regex expression
* Release of version 0.22.2
* Release of version 0.22.1
* All counts optional
* Include models using `fullmatch` instead of `search`
* Added option to exclude models from generated schema
* Update .thoth.yaml
* Release of version 0.22.0
* raise valueError
* Address issue #1573
* Avoid one join in the query
* Fix package symbols query
* Set default to False to reduce logging
* Fix inspection syncing for RHEL
* Fix OS name synced in container image analysis
* No need to query for package extract run - software environment can be directly used
* Alembic update
* Filter early
* outer join causing none values
* Refactor query for retrieving symbols in an image
* Make cuda version optional
* Simplified API functions
* Created query to monitor bloat data
* Fix method call to serialize models
* Fixed missing index issue
* Release of version 0.21.11
* Add missing keys to inspection schema validation
* new GitHub templates
* Added build log analysis result observations to graph database
* Release of version 0.21.10
* Make keys Optional
* Release of version 0.21.9
* Release of version 0.21.8
* Adjust parameter in query for PI
* Correct datatype
* Add missing key to sync inspections
* Set Packages Extract flag is_external to True always
* Missing change in query name to follow created standards
* Normalize OS version by discarding any minor release in RHEL release string
* Release of version 0.21.7
* Introduce a way to parametrize memory cache size
* Add index for solved table - it optimizes the has_solver_error query in adviser
* Release of version 0.21.6
* Release of version 0.21.5
* Alembic didn't create correct change in schema
* Release of version 0.21.4
* Consider only enabled indexes in unsolved queries
* Introduce a query for retrieving Python package entity names
* Release of version 0.21.3
* Release of version 0.21.2
* Release of version 0.21.1
* Fix parameter name for syncing provenance-checker documents
* Provide environment variable marker flag when retrieving transitive deps
* Correct inspection sync key
* Release of version 0.21.0
* Use datetime to sort results
* Fix advised software stack sync
* Format using black
* Drop id columns on relation tables
* Release of version 0.20.6
* Fix syncing external software environments coming from adviser
* Release of version 0.20.5
* Correct key from inspection output
* Missing randomize
* Adjust to follow naming convention
* Introduce software environment specific queries
* Release of version 0.20.4
* Release of version 0.20.3
* Fix syncs in versions
* Release of version 0.20.2
* Happy new year!
* Remove string size limitations from depends_on table
* Release of version 0.20.1
* :sparkles: added a PR template
* Fix keyword argument passing
* Release of version 0.20.0
* Do not show alembic info on configure_logger
* Super has no __del__
* Do not dispose engine in destructor
* Log number of dumps maintained
* Implement rotation of backups
* Fixes in reStructuredText in README file
* Release of version 0.19.30
* Release of version 0.19.29
* Increment solver error cache
* Increase cache for caching solver errors
* Remove unused indexes in depends_on table
* Fix Automatic Update Failure
* Sync cuda version
* Add missing filter
* Release of version 0.19.28
* Generalize function to retrieve multi values key metadata
* Add platforms
* WIP: Adjust Python Package Metadata query
* Add Thamos documentation
* Document automatic graph-backup job
* More formatting changes
* Minor docs reformatting
* Show database schema
* Provide is_s2i flag for adviser runs
* Point documentation to other libraries
* Add aggregated_at column to CVE
* Select distinct CVEs
* Adjust tests to new metadata
* Add deployment name to the result schema
* Release of version 0.19.27
* UBI:8 has optional variant_id
* Release of version 0.19.26
* Add Google Analytics
* Adjust testsuite
* Provide OS release schema
* Adjust default is_provided value
* Rename flag to is_provided_package_version
* Change Sphinx theme
* Correct staticmethod
* Release of version 0.19.25
* Increase characters metadata in keywords and summary metadata
* Optimize Analyzed Python Packages queries
* Optimnize unsolved queries
* Optimize queries
* Cache environment marker evaluation result
* :package: store database backup to ceph storage
* Fix Issue #1308 not iterable
* Fix alembic configuration instantiation issues
* Gather document id from document_id field
* :pushpin: Automatic dependency re-locking
* Use open instead of pathlib to adress PV in-cluster issues
* Make library thread safe
* Introduced sorting type in queries
* Fix wrong staticmethod
* Release of version 0.19.24
* Fix referencing store if is_local is set
* Add ability to sync documents based on absolute path
* Release of version 0.19.23
* Use context manager for handling sessions
* Fix warning for migration configuration check
* Release of version 0.19.22
* Correct output of queries
* Release of version 0.19.21
* Use same version as in the cluster
* Fix wrong rebase
* Dispose engine on disconnect
* Dispose engine on connect issues
* Release of version 0.19.20
* Use default pooling from sqlalchemy
* Adjust output query for metric
* Optimized/Improved query to retrieve unsolved Python Packages
* Fix schema check
* State ignoring a role assignment in docs
* Release of version 0.19.19
* Fix wrong propagation of is_local flag
* Increase character length for keywords metadata
* Release of version 0.19.18
* Correct attribute for metadata Provides-Extra
* Release of version 0.19.17
* Adjust sync for inspections
* Minor changes
* Release of version 0.19.16
* Pick metadata which were computed
* Grouped Metadata Distutils
* Created MetadataProvidesExtra
* Created MetadataProjectUrl
* Created MetadataRequiresExternal
* Created MetadataPlatform
* New models for PythonPackage Metadata that have multiple values
* Fix query to CVE for a given python package version entity
* Graph database cache has been removed
* Sync documents from a local directory if requested
* Release of version 0.19.15
* Randomize retrievals of unanalyzed Python packages
* Randomize retrieval of unsolved Python packages
* Correct errors for pytest
* Introduce enum classes for safe API
* Turn off checking thoth module by mypy
* Start using mypy in strict mode
* Fix retrieval of Python digests query
* Release of version 0.19.14
* Fix model for index url in the query
* Keep Python package tuples positional arguments
* Release of version 0.19.13
* Update naming queries according to Thoth convention
* Issue warning on connection to the database if schema is not up2date
* Update the schema
* Query to retrieve ML frameworks names
* Correct query to get metadata for Python Package
* HasArtifact is linked with PythonPackageVersionEntity table
* Revert "Symbol-API"
* Drop unique constraint in depends_on table
* added the registry to look for pgweb
* added podman-compose to dev packages list
* Fix model assignment when syncing results of Python interpreters
* Release of version 0.19.12
* Fixing the func argunment names
* consistency in using the variable force
* Fix index url issue, now properly
* Fix index_url key, now properly
* Fix version key dereference
* Fix index url key in new solvers implementation
* Release of version 0.19.11
* Handle issues in a better way
* Increase lines per file in Coala configuration
* Query environment markers stored in the database
* Add support for extras in the Python package dependencies retrieval query
* Introduce additional exception types for specific exceptions raised
* Drop cache support
* Updated .coafile to allow for longer files
* Coala errors
* More verbose errors, require all parameters
* Add offset and count
* Increase max lines per file
* Add api to get versioned symbols
* Get internal software & hardware environments
* Start using mypy for type checks
* Add missing provides-extra column to Python metadata
* Add missing columns to Python metadata
* Generic webhook updated to trigger the build from zuul
* Release of version 0.19.10
* Add update sync schema for PackageExtract
* Correct syncing issue
* Allow nullable software environemnts in the schema
* Fix multiple heads present
* Fix reference to variable in the query
* Fix query to retrieve number of unsolved packages
* Sync python interpreters
* Queries for packages with error in solvers and adjust schema
* Increase lenght file
* Added dependency monkey schema
* Added schema for package-extract sync
* Added solver sync schema
* Fix linkage of artifacts in Python package version entities
* Created adviser sync schema
* Add thoth sync schema for Amun
* Created docs for syncs inside Thoth Database
* Queries for packages with error in solvers and adjust schema
* Created solver functions following  naming convention
* Add missing import
* Remove unused import
* Created is_external for PackageExtractRun
* State how to implement syncing logic for any workload job done in the cluster
* Update syncs
* Changed schema and Added new Tables
* Update functions for metrics
* Add examples to docstrings
* Generate migration for new schema
* Convert function according to new naming convention
* Remove obsolete exception
* Expose sync_documents outside of module
* Implement a generic approach to sync any document
* Sync duration
* Generalized module varibale for count
* Created functions for get_python_packages cases
* Correct outputs
* New python_package_versions_count functions
* Hide query
* Added distinct flag
* New query
* get_python_package_version_count
* New queries for python packages
* Release of version 0.19.9
* Fix testsuite with recent changes
* Add duration to the result schema
* Release of version 0.19.8
* New query: count software stacks per type
* New queries
* Update queries
* Show an example run how to create a local PostgreSQL instance
* Use podman-compose
* Log what is being synced during graph syncs
* State graphviz package as a dependency when generating schema images
* Release of version 0.19.7
* Fix path to alembic versions - it has changed recently
* Allow limit latest versions to be None
* Make solver name optional when retrieving unsolved packages
* Introduce a check to verify the current database schema is up2date
* Drop also alembic version table
* Distribute alembic migrations with thoth-storages
* Release of version 0.19.6
* Add missing migrations to requirements.txt file
* Normalize Python package versions before each insert or query
* Make sure devs update to most recent version before generating new versions
* Make coala happy
* Use UTC when generating schema versions
* Generate initial schema using Alembic
* Start using Alembic for database migrations
* Add missing method used to register new packages in package releases
* Release of version 0.19.5
* Document how to dump and restore database in the running cluster
* Adjust logged message to inform about concurrent writes
* Randomize retrieval of unsolved Python packages
* Fix unsolved Python packages query
* Adjust signature of method to respect its return value
* Release of version 0.19.4
* Count and limit for advises can be nullable
* Increase advisory message for CVEs
* Release of version 0.19.3
* Disable connection pooling
* Release of version 0.19.2
* Update inspection sync for Upsert behaviour
* Implemented CASCADE on delete for Foreign Keys
* Release of version 0.19.1
* Release of version 0.19.0
* Remove accidentally committed file
* Add missing software stack relation to inspections
* Add missing import
* Disable cache inserts by default as they are expensive
* upsert-like logic
* Logic to sync inspection
* Increase lines allowed in a file
* Sync pacakge-analyzer results
* Sync system symbols detected by a package-extract
* Fix returned variable
* Check for solver errors before adding package to cache
* Start session with subtransactions enabled
* Be explicit about join
* Remove unique constraint
* Rewrite cache query to retrieved dependencies
* Raise NotFoundError if no records were found
* Implement method for listing analyses
* Implement method for getting analysis metadata
* Make methods which create data without starting transaction private
* Remove methods which should not be used outside of module
* Unify environment type handling
* Sync system symbols detected by a package-extract
* Reformat using black
* Introduce logic for syncing dependency-monkey documents
* Unify software stack creation handling
* Unify Python package version handling in PostgreSQL
* Move cache specific function to cache implementation
* Fix property name
* Introduce a new query which is used by adviser to filter out based on indexes
* Fix coala complains
* Remove old schema files
* Switch to PostgreSQL
* capture error
* Sync package analyzer error
* Add error flag to package analyzer run
* Remove index key
* Adjust tests to work with new implementation
* Do not raise exception, return None instead
* Call dgraph initialization
* Remove caching on top of Dgraph
* Remove accidentally committed file
* Mirror PostgreSQL with Dgraph for now
* PostgreSQL implementation
* Provide mechanism to clear in-memory cache
* Add entries to cache only if there were no solver errors
* Provide more information on cache statistics
* Use methodtools to properly handle lru cache on methods
* Use sqlite3 as cache
* Adjust query for retrieving transitive dependencies
* Adjust syncing logic to new depends_on schemantics
* Add is_provided flag
* Coala errors
* Store symbols
* Release of version 0.18.6
* Fix query for retrieving unsolved Python packages
* Minor changes to the function which returns unanalyzed packages
* Release of version 0.18.5
* Introduce a flag to retrieve only solved packages
* Use Python package name normalization from thoth-python module
* Release of version 0.18.4
* Fix Package Analyzer results syncing
* Fixes Syncing of Package Extract results
* Release of version 0.18.3
* Release of version 0.18.2
* Added missing inspection schema checks for voluptuous
* Release of version 0.18.1
* Solved conflict pinning to older version
* Corrected datatype-error for syncing
* Release of version 0.18.0
* New Dgraph function for PI
* Release of version 0.17.0
* Fix handling of pytest arguments in setup.py
* Revert changes in docker-compose
* Remove unused dependencies
* Rewrite querying logic for transitive dependencies retrieval
* Avoid copies when retrieving transitive dependencies
* Optimize retrieval of transitive queries
* Release of version 0.16.0
* Corrected voluptuous requirements for inspection schema:
* Modified Inspection schema
* Updated schema for PIConv
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
* Enable logging of graph database queries for debugging
* Fix handling of query filter
* Propagate OS information to runtime/buildtime environment nodes
* Update schema to capture os-release information
* Sync information about operating system captured in package-extract
* Update schema image respecting recent changes in PiMatmul
* Fix vertex cache handling
* Regenerate schema
* Add PythonFileDigest to schema documentation
* Introduce delete operation on top of models
* sync_package_analysis_documents
* Release of version 0.14.8
* Document schema hadnling in a living deployment
* Update dgraph.py
* Update README to show how to connect to the graph database from code
* Parametrize retrieval of unsolvable packages for the given solver
* Release of version 0.14.7
* Parametrize `@cascade` by `only_known_index` parameter
* Release of version 0.14.6
* Release of version 0.14.5
* Release of version 0.14.4
* Introduce retry exception on concurrent upsert writes
* :star: alphabetically order the files
* Release of version 0.14.3
* PackageAnalysisResultsStore is added
* Introduce pagination and solver_name filter
* Document local Dgraph instance setup
* Release of version 0.14.2
* Modified logic of the query to retrieve unsolved python packages for a given solver
* Update schema image for Thoth KG
* Update dgraph model schema for new parameters for PI
* Release of version 0.14.1
* Fix wrong variable reference
* Provide OS version and name as a string
* Release of version 0.14.0
* Ignore changelog file in coala, it's getting too large
* Release of version 0.13.0
* Release of version 0.12.0
* Removed unusued functions
* New UserHardwareInformation entity
* Update for Dgraph
* Check for cyclic dependencies in transitive query
* Fix number of overall results
* Qute fields as they are stored as strings
* Enhance exception information to give better information
* Release of version 0.11.4
* Fix normalization issue - normalize only package names
* An environment can have no analyses associated
* Release of version 0.11.3
* Provide method for buildtime environment listing
* Release of version 0.11.2
* Introduce mechanism to avoid gRPC issues when serializing large stacks
* Implement query for retrieving information about build-time errors
* Increase back-off count
* Implement back-off for random time in case of concurent upsert writes
* Release of version 0.11.1
* Fix computing edge hashes
* Created missing functions for Dgraph
* Normalize Python package names before inserting them into database
* Release of version 0.11.0
* Fix coala complains
* Implement query for retrieving transitive dependencies
* Fix python_sync_analysis
* Add missing provenance checker name
* Implement get_python_package_tuples for Dgraph
* Obsolete also unsolved_runtime_environments
* Remove obsolete queries
* Implemented get_all_versions_python_package method for Dgraph
* Add @normalize to flatten results
* Add @normalize to flatten results
* Add @normalize to flatten results
* Add normalization for package_name
* Added ecoystem filter
* Add Francesco to module authors
* Remove unused imports in dgraph.py implementation
* Implement query for retrieving artifact hashes from database
* Add query for checking provenance checker document id presence
* Implemment logic for checking if adviser run is present in db
* Fix query to retrieve solver count
* User software stack can have adviser or provenance-checker document id
* Implement query for retrieving image analysis count
* Implement query for retrieving solver error count
* Fix handling target UID for vertexes
* Implement runtime_environment_listing for Dgraph
* Retrieve read-only transaction for query operations
* Sync also digests when syncing solver documents
* Add missing annotations to models
* Remove checks which are already present in _create_python_package_record
* Fix syncing dependencies found in solver documents
* Schema proposal for Dgraph
* Add register_python_package_index to Dgraph implementation
* completed method for dgraph
* Introduce get_analysis_metadata for Dgraph
* Fix facets syntax when syncing edges dictionaries
* Implement get_python_package_index_urls for Dgraph
* Improve schema handling
* Switch to Dgraph
* Release of version 0.10.0
* New functions for janusgraph
* update schema file
* Fix coala complains
* Adjust method signatures
* Be consistent with return type, return always nan
* Update schema
* Error in query get_analyzer_documents_count()
* Add Thoth's configuration file
* Make runtime and buildtime environment names shared
* Release of version 0.9.7
* Use Sphinx for documentation
* Delete ceph.py.orig
* Fix solver error flag handling
* Add missing dot in Python version
* Respect errors in dependencies of packages
* Track solver_errors on depends_on edges
* Add missing ecosystem in query
* Remove duplicit definition
* black reformatted the file
* This repo requires Python 3.6
* Fix split count
* Fix solver name handling
* Add missing export from thoth.storages module
* Fix path to origin value of adviser and provenance-checker resutls
* Be consistent with property naming
* Update schema in docs
* Create relations between all the models in the graph database
* Introduce logic for syncing provenance check documents
* Adjust query to return unsolved packages for the given solver
* Update README with the most recent information about schema generation
* Increase number of lines per file
* Capture recommendation type in the graph model
* Introduce advised relationship
* Fix in markup
* State thoth-schema file path directly
* State automatic schema generation in README file
* Release of version 0.9.6
* Respect runtime environment in queries for direct dependencies
* Let callee preserve None values
* Consider hardware with no None values
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
* Depends on has to take account also environment
* Method can be static
* Adjust schema to reflect the current implementation
* Adjust solver related parts of schema for platform specifc features
* Provide method for solver name parsing
* Introduce flag exposing "existed" for Python package version
* Perform only graph or ceph sync if requested
* Move OpenShift specific bits to OpenShift
* Disconnect in destructor
* Avoid goblin model details in output
* Update README.rst
* Release of version 0.9.5
* Introduce name for a software stack
* Introduce query for querying software stacks
* Retrieve python package versions using asyncio
* ignoring some coala errors
* Reformat using black
* Do not handle exception twice
* Release of version 0.9.4
* Aggregate hashes from the graph database for the given package
* Performance index cannot be passed as None
* Fix query
* Version 0.9.3
* Include also requirements-test.txt in package
* Version 0.9.2
* Include requirements.txt when packaging
* Release of version 0.9.1
* Do not forget to install Amun for interaction with Amun
* Fixes for CI
* Consider index when retrieving transitive dependencies
* Include index url in the releases listing
* Release of version 0.9.0
* Corrected README file
* Introduce query for gathering sha256 hashes
* Hashes are positional argument
* Create digest entries in the graph database for python packages
* Add long description for PyPI
* Use index_url in the graph database
* Sync indexes into the graph database
* Update schema document
* Introduce has_artifact edge
* Artifact hashes in graph database
* Use base image name if there were not installed any native pkgs
* Report which inspection id is being synced
* Hardware can be even None
* Log about Amun results gathering
* Introduce graceful flag for inspection syncs
* Return directly list, not chain iterable
* Update schema in docs
* Do not forget to install Amun client
* Update schema docs
* Fix recent errors
* Fix errors
* Fix syntax error
* Be consistent with storage prefix naming
* Rename observation_document_id to inspection_document_id
* Introduce buildtime environment model
* Fix CI
* Fix CI
* Fix CI
* Adjust document_id gathering
* Introduce methods for checking documents based on id
* added a pyproject.toml to keep black happy
* using thoth's coala job
* using thoth-pytest job
* Fix pytest4 warning
* Update schema documentation
* Release of version 0.8.0
* Add a query to check for solved packages
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
* Release of version 0.7.4
* Fix unparseable solver result sync
* Release of version 0.7.3
* Correctly handle decorator wrappers
* Introduce dependency monkey reports adapter
* Fix query to retrieve all package versions
* Fix document naming
* Fix CI failures
* Rename error flags
* Introduce unparsed flag
* Introduce unparsed flag
* Keep schema up2date with recent schema changes
* Hostname is not equal to document id
* Introduce transitive dependencies gathering method
* Normalize names of packages that are inserted into graph database
* Release of version 0.7.2
* Introduce unsolvable flag
* Release of version 0.7.1
* Release of version 0.7.0
* Use job id as document id instead of pod id
* Implement image lookup for fast checks of image analyses
* Release of version 0.6.0
* Remove ignore comments
* Fix CI
* Add timestamp to the result schema
* Release of version 0.5.4
* Edge property is not a vertex property
* Release of version 0.5.3
* Update README file
* Introduce query for gathering dependencies
* Specify Python index from which the package came from
* Introduce check whether the given Python package exists
* Release of version 0.5.2
* Revert to the last release
* Revert "Release of version 0.5.6"
* Release of version 0.5.6
* Release of version 0.5.5
* Update .zuul.yaml
* Release of version 0.5.4
* Release of version 0.5.3
* Update janusgraph.py
* Sync debian packages to the graph database
* Release of version 0.5.2
* Revert "put it in zuul's user-api queue"
* put it in zuul's user-api queue
* change the queue
* change the queue
* Create adapter for provenance reports
* Release of version 0.5.1
* Store information about Python vulnerabilities
* Fix missing import
* added VSCode directory to git ignore list
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
* Initial dependency lock
* Delete Pipfile.lock for relocking dependencies
* Update .zuul.yaml
* removing pydocstyle
* preparing release 0.0.33
* removing unneeded E501
* Version 0.0.32
* Version 0.0.31
* added the gate pipeline to the core queue
* preparing for a zuul driven, fully coala compliant 0.0.30 release
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
* Ignore eggs in coala
* Run coala in non-interactive mode
* Make coala happy again
* Run coala in CI
* Version 0.0.26
* Test Ceph/S3 adapters against mocked environment
* Update .gitignore
* Tests for cache
* Be consistent with indentation
* Different botocore versions behave differently
* Tests for Ceph adapter
* Test result schema
* Correctly propagate connection check to Ceph adapter
* Provide a way to specify bucket prefix explicitly
* Create initial tests
* Introduce Ceph connection check
* Fix yarl issues
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
* Check for object existence
* Preperly return property value
* Use __properties__ instead of __dict__
* Fix missing self reference
* Version 0.0.21
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
* Introduce a function to find PyPI packages that deps were not resolved
* Add README file
* Version 0.0.18
* Version 0.0.17
* Provide routines to check solver results or analysis results presence
* Add spaces after equal sign
* Version range should be always stated
* Also state package name on depends_on edge
* Filter out irrelevant artifact requirements.txt from sync
* Version 0.0.16
* Fix wrong attribute reference
* Version 0.0.15
* Fix wrong property name
* Add missing attributes during sync
* Fix ecosystem name
* Be more sensitive with sync errors
* Fix missing argument
* Fix property types
* Bump schema docs version
* Update schema docs
* Revisit graph sync
* Version 0.0.14
* Remove nested .gitignore
* Respect changes in schema renaming
* Package version is now package_version
* Package version is now package_version
* Unify property naming
* Schema documentation
* Fix behavior in Jupyter notebooks to respect env variables
* Make caching configurable
* Implement cache handling
* Provide a way to specify source_id/target_id explicitly
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
* Version 0.0.7
* Add adapter for build logs
* Add method for iterating over results in Ceph
* Version 0.0.6
* Abstract document_id handling logic
* Abstract prefix creation
* Version 0.0.5
* Do not create bucket on Ceph for now
* Use RESULT_TYPE field to distinguish between database adapters
* Add missing dependnecy - boto3
* Require keyword arguments for constructor
* Create Ceph adapter
* State only direct requirements in requirements.txt
* Make the g object accessible for the graph access
* Use new create() methods to be consistent
* Version 0.0.4
* Rename JanusGraphDatabase to GraphDatabase
* Update requirements.txt
* Version 0.0.3
* Add forgotten dependency
* Version 0.0.2
* Version 0.0.1
* Add logic to iterate over available results
* State all packages in requirements file
* Do not check requirements hashes for now
* Fix docstring
* Add .gitignore
* Implement analysis results store adapter
* Implement solver results store adapter
* Implement disconnecting logic
* Create initial classes with interface
* Add .travis.yml configuration file
* Initial project import
### Bug Fixes
* Raise an exception when the given record was not found (#2069)
* Alembic timeline fix (#2035)
* Fix logging error when database schema is not up2date (#1949)
* Default platform if not available in the solver document (#1901)
* Update lock file to fix issues in CI
* fixed re-active
* fixed typo and changed migrations
* pytest failing due to hash mismatch
* Corrected wrong keys used in solver sync
* Relock to fix sqlalchemy release hashes
* join with PythonSoftware not external
* Add check in sync when report is not provided by Adviser
* Sync missing packages if adviser failed due to unknown dependencies
* normalize, distinct, fix index
* Adjust syncing logic of Dependency Monkey documents based on the current output
* Fix wrong argument name propagated
* Do not sync package errors if the given package is not provided
* Optimized Solved quries with error
* Issue warning instead of error
* Fix bug in checking for dist key
* Relax fatal error on syncing unmatched metadata
* Issue warning if the database schema is not initialized yet in connect
* Fix error when case 3 is not declared yet
* Raise not found error if the given Python index is not found
* Minor fix to address typo
* Minor typo fixes in README file
* Minor fixes to make dependency monkey syncs work properly
* Fix invalid foreign key error on schema creation
* Use indexes and minor fixes
* Retrieve packages that are not analyzed by Package-Analyzer
* Fix key error 'python'
* Quote user input parts of the query in error message produced
* Check if the given package in the given version was solved by specific solver
* Provide better exception message on parsing error
* Fix wrong indentation in adviser results sync
* Minor fix to display correct release in title of docs html
* Fix missing import causing issues in graph-sync-job
* Return None if no entity was found for in query_one
* Fix issues reported by coala runs
* Remove failing test
* Reformat using black, fix some coala warnings
* fix one check
* Fixed output after tests
* Minor code fixes
* Turn ram size into float to fix serialization/deserialization issues
* Adjust query to track solver errors on the given runtime env
* fixing some coala errors
* Introduce adviser error flag in user stack
* If adviser analysis was not succesfull no lockfile is provided
* Minor fixes in method signatures
* Linter fixes
* Do not query graph database if no id is provided
* Fix key error if hardware was not provided on Amun
* fixed some coala problems
* fixing project.post.jobs.trigger-build.vars.webhook_url
* using envvar that are injected by OpenShift to discover janusgraph servcie host and port, this requires that a service called "janusgraph" is created
* fixed line too long
* some pytest fixed wrt the prefix
* some pylint fixed
* Modify requirements to fix yarl issues
* Skip mercator errors that are not stored anyway
* Improve error handling
* Fix issue with vertex property being stored instead of its value
* Revisit key error fix
* A temporary fix for mercator result being None
* Fix key error when syncing to graph database
* Log exception instead of error
* Log exception instead of error
* Fix error when syncing data to janusgraph with VertexProperty
* Fix wrong model name
* Fix wrong parameter
* Raise appropriate exception on non-existing key
* Raise an exception on invalid schema
### Improvements
* check for cuda nvcc and found in file version (#2092)
* :arrow_down: removed the files as they are no longer required
* change flag name and alembic commands (#2033)
* Add query for adviser run per source type (#1997)
* Make package version and package index optional in get_depends_on (#1975)
* State how to install podman and podman-compose (#1971)
* Introduce method for retrieving inspection ids and count (#1879)
* Create queries for SI retrieval for certain package name, version , index (#1882)
* make coala happy
* No inspection result batch size
* Reproduce methods specific for postgres
* Adjust methods
* more info
* Fix computing batch size of inspection jobs
* break security indicators into two stores
* Add routines and index for platform manipulation
* create class for storing security indicators
* Fix typo
* Raise NotFoundError if setting is_missing flag for non-existing package
* docstring match variable name
* function for checking current availability of package
* Adjust method name based on review comment
* Add logic for syncing revsolver result
* Small typo
* Modified logic for adviser sync
* Modify schema and logic to sync adviser run
* Update storages function to be more versatile and follow conventions
* Remove unnecessary imports
* Add doc strings and remove unnecessary subtransactions
* Python must have major and minor version
* Fix index creation for symbols queries
* Change from externalsoftware environment, and uncouple id index
* Move cache to storage level
* Add indexes to improve abi queries
* Fix reference to variable
* added some files to gitignore
* :sweat_smile: Auto pip and black formatting
* Create index for has_artifact table
* Adjust index for PPV combinations
* Fix query for enabled index
* Query for index_url before creating index
* Adjust datatype for conv PI to sync inspection results
* Do not use id when counting tables
* Create index for CVE step to omit sequence scan
* correct typo
* Sync package version requested rather than package version reported
* Optimize marker evaluation result query for adviser
* Adjust names of parameters to respect their semantics
* Introduce PyBench PI table and adjust sync logic for inspection
* Make some log info optional
* Create index for get_depends_on query
* Adjust tests to the new implementation
* Remove self to make method static
* Introduce ping method
* :green_heart: added more builds that need to be triggered
* Standardize sync logic entries for Adviser, Provenance Checker and Dependency Monkey
* Added MetadataDistutils, updated sync logic, schema docs, Tested syncs
* Created MetadataRequiresDist and MetadataSupportedPlatform
* Cache some of the query results
* Remove old pydgraph dependency
* Add normalization for package_name and package_version
* Standardize and unify query for python artifact hashes
* State maintainer and project url in setup.py
* Sync container image size
* Fixing the func argunment design
* Introduce query for checking marker evaluation results
* Remove graph cache tests
* Fix signature of the private method - unsolved edge cases
* Created query for python package metadata for user-api
* Created and updated queries for analyzed packages
* New schema and sync in Solver for PythonPackageMetadata
* Consistenly sync index_url and package_version
* Added schema for package extract
* Added provenance checker sync and all components sync
* Updated and tested all solved/unsolved functions
* Remove old file for Dgraph related tests
* Add logic for syncing marker and extra
* No NULL values for some PythonPackageVersion attributes
* We use psql not pg_restore
* Fix small typo
* New class methods for InspectionStore
* Provide method for disabling and enabling Python package index
* Remove unused imports
* State how to print stats to logs in README file
* Log statistics of graph cache and memory cache if requested so
* Use more generic env variable names
* Add tests and adjust existing testsuite to respect cache flags
* Updates for consistency
* Fix cache test
* Remove debug warnings accidentally committed
* Package version can have some of the values None
* Remove unused parameters
* Implement logic for syncing adviser results
* Fix typos
* Implement logic for syncing provenance checker results
* Implement logic for syncing package-extract results
* updated schema
* Add statistics of queries to sqlite3 cache
* Optimize two queries into one and iterate over all configurations resolved
* Do not use slots as LRU cache wrappers fail
* Provide adapter for storing and restoring graph cache in builds
* Introduce cache for caching results of well-used packages
* Provide method for counting number of unsolved Python packages
* Add models for versioned symbols and associated edges
* Add PI for Conv1D and Conv2D for tensorflow
* Remove old test
* sync package analyzer results
* Update schema to include package analyzer
* State in the README file how to debug graph database queries
* Fix typo in matrix
* Add standard project template and code owners
* Rename models and properties
* Fix refactoring typo
* Introduce method for creating Python package version entities
* :dizzy: updated adapters for storing buillog analysis results and cache
* Require non-null `index_url` and `package_name`
* New tests for inspection schema check before sync
* code-style and new functions
* New sync logic for PI
* Update schema, functions and design schema
* Correct typo
* Reorganize Python package creation
* Remove unused method
* Implemented runtime_environment_analyses_listing method for Dgraph
* Implemented retrieve_unsolved_pypi_packages method for Dgraph
* Implemented retrieve_dependent_packages method for Dgraph
* Implemented retrieve_solved_pypi_packages method for Dgraph
* Implemented retrieve_unsolvable_pypi_packages method for Dgraph
* Fix typos
* Implemented retrieve_unparsable_pypi_packages method for Dgraph
* Implemented get_all_python_package_version_hashes_sha256 method for Dgraph
* Implemented python_package_exists method for Dgraph
* Implemented python_package_version_exists method for Dgraph
* Implemented get_python_packages_for_index method for Dgraph
* Implemented get_python_packages method for Dgraph
* Implemented analysis_records_exist method for Dgraph
* Implemented solver_records_exist method for Dgraph
* Fix get_analysis_metadata function, sync_functions, models and graph schema
* Implement method for gathering CVEs for Python packages
* Add query for checking presence of inspection runs
* Implement logic for querying for DependencyMonkey document presence
* Implement logic for checking image analysis run presence
* Fix query for checking solver document presence
* minor change
* Implemented get_all_python_packages_count method for Dgraph
* Introduce solver_document_id_exist method for Dgraph
* Fix sync of edge sync - source and target should not be part of sync
* New Edge between PythonPackageVersion and PythonPackageIndex
* Distinguish between runtime and buildtime environment
* Remove duplicit method
* Fix clash of runtime environment - model versus representing class
* Add type to queries to hit index
* :bug: removed the trailing slash
* Fix coala warnings
* this part of the path is no longer required
* Add CVE name when querying for CVEs
* Add python version and cuda version to graph schema
* Introduce adapter for storing caching analysis ids based on image digest
* Introduce method for gathering packages known to thoth based on index
* Do not rely in Gremlin queries for order of received items
* Fix typo in retrieve_dependencies(...) query
* Remove unused imports
* Assign index to all packages in inspection sync
* Normalize python package names before every graph operation
* Add index url to the check for Python package version existance
* Update README to include test suite in setup.py
* Use models to_dict method to obtain values
* Fix Python package index URL retrieval
* Add method for retrieving Python package index URLs
* Introduce method for registering Python package indexes
* Introduce method for syncing inspection documents
* Remove runtime and buildtime observations
* Create method for syncing inspections into janusgraph
* Do not use schema for inspections
* Remove unused variable
* Introduce sync methods
* Introduce adapter for inspection results
* Return also python package index model
* Introduce method for creating Python package index vertex
* Add python package index entity
* Add method for counting documents
* Add methods in janusgraph for metrics
* Exclude test directory
* Introduce methods for checking unsolvable and unparsed packages
* Introduce method for gathering python package versions
* Introduce observation models and adapter
* Fix variable name
* Change in variable names
* Run tests in Travis CI
* Add test dependencies
* Fix assertion test
* Abstract common code to a base class
* No need to copy env variables
* Add base class for tests
* Implement tests for build logs adapter
* Expose adapter for adviser results
* Introduce adapter for adviser for recommendations
* Introduce to_pretty_dict() method
* Introduce logic that wraps PyPI package creation
* Make sure we use correct attributes
* Log correct variable
* Use VertexProperty class for Vertex properties
* Initial schema creation and graph sync
* Reuse logic from result store base adapter in solver result adapter
* Reuse logic in analysis adapter from result base adapter
* Create result base for storing raw results onto Ceph
* Add base classes for vertex and edges to cover common logic
* Fix typo
* Create storage base class
* Add result schema for analyzer results
* Add docstrings for result store methods.
* Improve logging + refactor defaults
* Implement graph storing logic for JanusGraph
### Non-functional
* Add security and performance database enums (#1940)
* Drop methods tools to gain performance
* Adjust model performance for inspection output
* Fix performance indicator name
* Fix documentation for performance indicators
* Drop performance related query
* Adjust query for retrieving performance indicators
* Count number of performance indicators based on framework
* Introduce method for counting performance indicator entries
* Do not maintain schema for performance indicators
* Substitute from_properties with get_or_create in performance models
* Update schema based on updates to performance indicators
* Unify schema for creating performance indicators and their handling
* Use index for int values of performance indicators
* Always return float when computing average performance
* Implement method for gathering average performance
* Adjust performance query to respect runtime environment
* Extend performance query so it is more generic
* Improve handling of performance index
* Sync also performance index to janusgraph
* Introduce query for computing performance index
* Gather performance index from inspection jobs
* Rename failure test case for better readability
* Improving Goblin's driver performance
### Other
* remove variables
* remove imports
* remove sqlalchemy utils
* Remove duplicate entry
* Fix wrong base class
* Do not duplicate logic
* Use coala for code checks
* Refactor code to export defaults
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.16.12 to 1.16.15 (#2089)
* :pushpin: Automatic update of dependency boto3 from 1.16.11 to 1.16.12 (#2087)
* :pushpin: Automatic update of dependency boto3 from 1.16.10 to 1.16.11 (#2082)
* :pushpin: Automatic update of dependency boto3 from 1.16.10 to 1.16.11 (#2081)
* :pushpin: Automatic update of dependency boto3 from 1.16.9 to 1.16.10 (#2076)
* :pushpin: Automatic update of dependency boto3 from 1.16.8 to 1.16.9
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#2062)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#2061)
* :pushpin: Automatic update of dependency boto3 from 1.16.6 to 1.16.8 (#2060)
* :pushpin: Automatic update of dependency boto3 from 1.16.0 to 1.16.6 (#2057)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#2056)
* :pushpin: Automatic update of dependency boto3 from 1.15.16 to 1.16.0 (#2055)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#2053)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#2052)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.19 to 1.3.20 (#2051)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1
* :pushpin: Automatic update of dependency boto3 from 1.15.11 to 1.15.16
* :pushpin: Automatic update of dependency boto3 from 1.15.9 to 1.15.11 (#2043)
* :pushpin: Automatic update of dependency boto3 from 1.15.8 to 1.15.9 (#2041)
* :pushpin: Automatic update of dependency boto3 from 1.15.7 to 1.15.8 (#2034)
* :pushpin: Automatic update of dependency boto3 from 1.15.6 to 1.15.7 (#2026)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#2023)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#2020)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#2019)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#2018)
* :pushpin: Automatic update of dependency boto3 from 1.15.1 to 1.15.6 (#2017)
* :pushpin: Automatic update of dependency voluptuous from 0.11.7 to 0.12.0 (#2011)
* :pushpin: Automatic update of dependency boto3 from 1.14.63 to 1.15.1 (#2012)
* :pushpin: Automatic update of dependency boto3 from 1.14.62 to 1.14.63 (#2009)
* :pushpin: Automatic update of dependency boto3 from 1.14.61 to 1.14.62 (#2006)
* :pushpin: Automatic update of dependency boto3 from 1.14.61 to 1.14.62 (#2004)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#1996)
* :pushpin: Automatic update of dependency thoth-common from 0.18.2 to 0.19.0 (#1999)
* :pushpin: Automatic update of dependency boto3 from 1.14.60 to 1.14.61 (#1998)
* :pushpin: Automatic update of dependency alembic from 1.4.2 to 1.4.3 (#1991)
* :pushpin: Automatic update of dependency alembic from 1.4.2 to 1.4.3 (#1990)
* :pushpin: Automatic update of dependency thoth-common from 0.18.1 to 0.18.2 (#1989)
* :pushpin: Automatic update of dependency boto3 from 1.14.58 to 1.14.60 (#1988)
* :pushpin: Automatic update of dependency thoth-common from 0.18.0 to 0.18.1 (#1983)
* :pushpin: Automatic update of dependency thoth-common from 0.17.3 to 0.18.0 (#1982)
* :pushpin: Automatic update of dependency boto3 from 1.14.57 to 1.14.58 (#1981)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.2 (#1973)
* :pushpin: Automatic update of dependency boto3 from 1.14.49 to 1.14.53 (#1972)
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#1970)
* :pushpin: Automatic update of dependency boto3 from 1.14.47 to 1.14.49 (#1969)
* :pushpin: Automatic update of dependency boto3 from 1.14.46 to 1.14.47 (#1956)
* :pushpin: Automatic update of dependency boto3 from 1.14.45 to 1.14.46 (#1950)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.18 to 1.3.19 (#1943)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#1942)
* :pushpin: Automatic update of dependency boto3 from 1.14.43 to 1.14.45 (#1941)
* :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#1935)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#1934)
* :pushpin: Automatic update of dependency pytest from 6.0.0 to 6.0.1 (#1933)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#1932)
* :pushpin: Automatic update of dependency boto3 from 1.14.31 to 1.14.43 (#1931)
* :pushpin: Automatic update of dependency thoth-common from 0.15.0 to 0.16.0 (#1924)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0 (#1921)
* :pushpin: Automatic update of dependency boto3 from 1.14.30 to 1.14.31 (#1920)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.15.0 (#1915)
* :pushpin: Automatic update of dependency boto3 from 1.14.28 to 1.14.30 (#1914)
* :pushpin: Automatic update of dependency boto3 from 1.14.26 to 1.14.28 (#1912)
* :pushpin: Automatic update of dependency boto3 from 1.14.22 to 1.14.26 (#1908)
* :pushpin: Automatic update of dependency boto3 from 1.14.21 to 1.14.22 (#1903)
* :pushpin: Automatic update of dependency pytest-timeout from 1.4.1 to 1.4.2 (#1900)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#1899)
* :pushpin: Automatic update of dependency boto3 from 1.14.19 to 1.14.21 (#1898)
* :pushpin: Automatic update of dependency boto3 from 1.14.18 to 1.14.19 (#1894)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.7 to 0.36.8 (#1889)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.7 to 0.36.8 (#1887)
* :pushpin: Automatic update of dependency boto3 from 1.14.17 to 1.14.18 (#1886)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.6 to 0.36.7 (#1876)
* :pushpin: Automatic update of dependency thoth-common from 0.14.0 to 0.14.1 (#1875)
* :pushpin: Automatic update of dependency boto3 from 1.14.14 to 1.14.17 (#1874)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.0 (#1872)
* :pushpin: Automatic update of dependency boto3 from 1.14.13 to 1.14.14 (#1866)
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13 (#1865)
* :pushpin: Automatic update of dependency boto3 from 1.14.9 to 1.14.13 (#1864)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.17 to 1.3.18
* :pushpin: Automatic update of dependency boto3 from 1.14.4 to 1.14.9
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.11 to 0.13.12
* :pushpin: Automatic update of dependency boto3 from 1.13.24 to 1.14.1
* :pushpin: Automatic update of dependency boto3 from 1.13.23 to 1.13.24
* :pushpin: Automatic update of dependency boto3 from 1.13.22 to 1.13.23
* :pushpin: Automatic update of dependency boto3 from 1.13.21 to 1.13.22
* :pushpin: Automatic update of dependency boto3 from 1.13.20 to 1.13.21
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* :pushpin: Automatic update of dependency boto3 from 1.13.19 to 1.13.20
* :pushpin: Automatic update of dependency boto3 from 1.13.18 to 1.13.19
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency boto3 from 1.13.17 to 1.13.18
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency boto3 from 1.13.16 to 1.13.17
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.5 to 0.36.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency boto3 from 1.13.15 to 1.13.16
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency boto3 from 1.13.14 to 1.13.15
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.13 to 1.13.14
* :pushpin: Automatic update of dependency boto3 from 1.13.12 to 1.13.13
* :pushpin: Automatic update of dependency boto3 from 1.13.11 to 1.13.12
* :pushpin: Automatic update of dependency boto3 from 1.13.10 to 1.13.11
* :pushpin: Automatic update of dependency boto3 from 1.13.6 to 1.13.9
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.16 to 1.3.17
* :pushpin: Automatic update of dependency boto3 from 1.13.5 to 1.13.6
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic update of dependency boto3 from 1.13.4 to 1.13.5
* :pushpin: Automatic update of dependency boto3 from 1.13.3 to 1.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.2 to 1.13.3
* :pushpin: Automatic update of dependency boto3 from 1.12.47 to 1.12.49
* :pushpin: Automatic update of dependency click from 7.1.1 to 7.1.2
* :pushpin: Automatic update of dependency boto3 from 1.12.46 to 1.12.47
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* :pushpin: Automatic update of dependency boto3 from 1.12.43 to 1.12.46
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* :pushpin: Automatic update of dependency boto3 from 1.12.38 to 1.12.39
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.15 to 1.3.16
* :pushpin: Automatic update of dependency boto3 from 1.12.37 to 1.12.38
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* :pushpin: Automatic update of dependency boto3 from 1.12.36 to 1.12.37
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.4 to 2.8.5
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.0 to 0.6.1
* :pushpin: Automatic update of dependency boto3 from 1.12.35 to 1.12.36
* :pushpin: Automatic update of dependency boto3 from 1.12.34 to 1.12.35
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency boto3 from 1.12.33 to 1.12.34
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.12.4 to 0.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.32 to 1.12.33
* :pushpin: Automatic update of dependency boto3 from 1.12.31 to 1.12.32
* :pushpin: Automatic update of dependency boto3 from 1.12.30 to 1.12.31
* :pushpin: Automatic update of dependency thoth-common from 0.12.3 to 0.12.4
* :pushpin: Automatic update of dependency boto3 from 1.12.29 to 1.12.30
* :pushpin: Automatic update of dependency thoth-common from 0.12.2 to 0.12.3
* :pushpin: Automatic update of dependency pyyaml from 5.3.1 to 3.13
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.28 to 1.12.29
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.1
* :pushpin: Automatic update of dependency boto3 from 1.12.27 to 1.12.28
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* :pushpin: Automatic update of dependency boto3 from 1.12.26 to 1.12.27
* :pushpin: Automatic update of dependency boto3 from 1.12.25 to 1.12.26
* :pushpin: Automatic update of dependency alembic from 1.4.1 to 1.4.2
* :pushpin: Automatic update of dependency boto3 from 1.12.24 to 1.12.25
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* :pushpin: Automatic update of dependency boto3 from 1.12.23 to 1.12.24
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.2 to 0.36.3
* :pushpin: Automatic update of dependency boto3 from 1.12.22 to 1.12.23
* :pushpin: Automatic update of dependency boto3 from 1.12.21 to 1.12.22
* :pushpin: Automatic update of dependency pytest from 5.3.5 to 5.4.1
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.1 to 0.36.2
* :pushpin: Automatic update of dependency pytest-mypy from 0.5.0 to 0.6.0
* :pushpin: Automatic update of dependency boto3 from 1.12.20 to 1.12.21
* :pushpin: Automatic update of dependency pyyaml from 5.3 to 3.13
* :pushpin: Automatic update of dependency boto3 from 1.12.19 to 1.12.20
* :pushpin: Automatic update of dependency boto3 from 1.12.18 to 1.12.19
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.14 to 1.3.15
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.13 to 1.3.14
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* :pushpin: Automatic update of dependency click from 7.0 to 7.1.1
* :pushpin: Automatic update of dependency boto3 from 1.12.16 to 1.12.18
* :pushpin: Automatic update of dependency boto3 from 1.12.10 to 1.12.11
* :pushpin: Automatic update of dependency boto3 from 1.12.9 to 1.12.10
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* :pushpin: Automatic update of dependency boto3 from 1.12.8 to 1.12.9
* :pushpin: Automatic update of dependency boto3 from 1.12.7 to 1.12.8
* :pushpin: Automatic update of dependency boto3 from 1.12.6 to 1.12.7
* :pushpin: Automatic update of dependency amun from 0.4.0 to 0.4.3
* :pushpin: Automatic update of dependency boto3 from 1.12.5 to 1.12.6
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.2 to 0.5.0
* :pushpin: Automatic update of dependency boto3 from 1.12.4 to 1.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.3 to 1.12.4
* :pushpin: Automatic update of dependency boto3 from 1.12.2 to 1.12.3
* :pushpin: Automatic update of dependency amun from 0.3.8 to 0.4.0
* :pushpin: Automatic update of dependency boto3 from 1.12.1 to 1.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.0 to 1.12.1
* :pushpin: Automatic update of dependency boto3 from 1.11.17 to 1.12.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency boto3 from 1.11.16 to 1.11.17
* :pushpin: Automatic update of dependency boto3 from 1.11.15 to 1.11.16
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* :pushpin: Automatic update of dependency boto3 from 1.11.14 to 1.11.15
* :pushpin: Automatic update of dependency boto3 from 1.11.13 to 1.11.14
* :pushpin: Automatic update of dependency boto3 from 1.11.12 to 1.11.13
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency boto3 from 1.11.11 to 1.11.12
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic update of dependency boto3 from 1.11.10 to 1.11.11
* :pushpin: Automatic update of dependency alembic from 1.3.3 to 1.4.0
* :pushpin: Automatic update of dependency boto3 from 1.11.9 to 1.11.10
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* :pushpin: Automatic update of dependency amun from 0.3.7 to 0.3.8
* :pushpin: Automatic update of dependency amun from 0.3.6 to 0.3.7
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency amun from 0.3.5 to 0.3.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* :pushpin: Automatic update of dependency boto3 from 1.11.8 to 1.11.9
* :pushpin: Automatic update of dependency boto3 from 1.11.7 to 1.11.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.12 to 1.3.13
* :pushpin: Automatic update of dependency alembic from 1.3.2 to 1.3.3
* :pushpin: Automatic update of dependency boto3 from 1.11.6 to 1.11.7
* :pushpin: Automatic update of dependency amun from 0.3.4 to 0.3.5
* :pushpin: Automatic update of dependency amun from 0.3.3 to 0.3.4
* :pushpin: Automatic update of dependency boto3 from 1.11.5 to 1.11.6
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* :pushpin: Automatic update of dependency boto3 from 1.11.4 to 1.11.5
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency amun from 0.3.2 to 0.3.3
* :pushpin: Automatic update of dependency boto3 from 1.11.3 to 1.11.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.28
* :pushpin: Automatic update of dependency amun from 0.3.1 to 0.3.2
* :pushpin: Automatic update of dependency boto3 from 1.11.2 to 1.11.3
* :pushpin: Automatic update of dependency boto3 from 1.11.1 to 1.11.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* :pushpin: Automatic update of dependency boto3 from 1.11.0 to 1.11.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* :pushpin: Automatic update of dependency amun from 0.3.0 to 0.3.1
* :pushpin: Automatic update of dependency boto3 from 1.10.50 to 1.11.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* :pushpin: Automatic update of dependency amun from 0.2.7 to 0.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.49 to 1.10.50
* :pushpin: Automatic update of dependency thoth-python from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency boto3 from 1.10.48 to 1.10.49
* :pushpin: Automatic update of dependency thoth-python from 0.8.0 to 0.9.0
* :pushpin: Automatic update of dependency boto3 from 1.10.47 to 1.10.48
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* :pushpin: Automatic update of dependency thoth-python from 0.7.1 to 0.8.0
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.3 to 1.3.4
* :pushpin: Automatic update of dependency pyyaml from 5.2 to 5.3
* :pushpin: Automatic update of dependency boto3 from 1.10.46 to 1.10.47
* :pushpin: Automatic update of dependency boto3 from 1.10.45 to 1.10.46
* :pushpin: Automatic update of dependency boto3 from 1.10.44 to 1.10.45
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.0 to 0.36.1
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency boto3 from 1.10.43 to 1.10.44
* :pushpin: Automatic update of dependency boto3 from 1.10.42 to 1.10.43
* :pushpin: Automatic update of dependency boto3 from 1.10.41 to 1.10.42
* :pushpin: Automatic update of dependency boto3 from 1.10.40 to 1.10.41
* :pushpin: Automatic update of dependency alembic from 1.3.1 to 1.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.39 to 1.10.40
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.11 to 1.3.12
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.38 to 1.10.39
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency boto3 from 1.10.35 to 1.10.38
* :pushpin: Automatic update of dependency boto3 from 1.10.34 to 1.10.35
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.35.0 to 0.36.0
* :pushpin: Automatic update of dependency boto3 from 1.10.33 to 1.10.34
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency boto3 from 1.10.32 to 1.10.33
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* :pushpin: Automatic update of dependency boto3 from 1.10.31 to 1.10.32
* :pushpin: Automatic update of dependency boto3 from 1.10.30 to 1.10.31
* :pushpin: Automatic update of dependency boto3 from 1.10.29 to 1.10.30
* :pushpin: Automatic update of dependency pyyaml from 5.1.2 to 5.2
* :pushpin: Automatic update of dependency boto3 from 1.10.28 to 1.10.29
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.19
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* :pushpin: Automatic update of dependency boto3 from 1.10.26 to 1.10.27
* :pushpin: Automatic update of dependency sqlalchemy-stubs from 0.2 to 0.3
* :pushpin: Automatic update of dependency boto3 from 1.10.25 to 1.10.26
* :pushpin: Automatic update of dependency boto3 from 1.10.24 to 1.10.25
* :pushpin: Automatic update of dependency boto3 from 1.10.23 to 1.10.24
* :pushpin: Automatic update of dependency boto3 from 1.10.22 to 1.10.23
* :pushpin: Automatic update of dependency boto3 from 1.10.21 to 1.10.22
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.20 to 1.10.21
* :pushpin: Automatic update of dependency boto3 from 1.10.19 to 1.10.20
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* :pushpin: Automatic update of dependency boto3 from 1.10.18 to 1.10.19
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency boto3 from 1.10.17 to 1.10.18
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* :pushpin: Automatic update of dependency boto3 from 1.10.16 to 1.10.17
* :pushpin: Automatic update of dependency alembic from 1.3.0 to 1.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* :pushpin: Automatic update of dependency boto3 from 1.10.15 to 1.10.16
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.10 to 1.3.11
* :pushpin: Automatic update of dependency boto3 from 1.10.14 to 1.10.15
* :pushpin: Automatic update of dependency boto3 from 1.10.13 to 1.10.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.5 to 0.7.1
* :pushpin: Automatic update of dependency boto3 from 1.10.12 to 1.10.13
* :pushpin: Automatic update of dependency boto3 from 1.10.11 to 1.10.12
* :pushpin: Automatic update of dependency boto3 from 1.10.10 to 1.10.11
* :pushpin: Automatic update of dependency boto3 from 1.10.9 to 1.10.10
* :pushpin: Automatic update of dependency python-dateutil from 2.8.1 to 2.8.0
* :pushpin: Automatic update of dependency boto3 from 1.10.8 to 1.10.9
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.1 to 0.4.2
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency boto3 from 1.10.7 to 1.10.8
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.34.2 to 0.35.0
* :pushpin: Automatic update of dependency boto3 from 1.10.6 to 1.10.7
* :pushpin: Automatic update of dependency alembic from 1.2.1 to 1.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.5 to 1.10.6
* :pushpin: Automatic update of dependency boto3 from 1.10.4 to 1.10.5
* :pushpin: Automatic update of dependency boto3 from 1.10.3 to 1.10.4
* :pushpin: Automatic update of dependency boto3 from 1.10.2 to 1.10.3
* :pushpin: Automatic update of dependency methodtools from 0.1.1 to 0.1.2
* :pushpin: Automatic update of dependency pytest from 5.2.1 to 5.2.2
* :pushpin: Automatic update of dependency boto3 from 1.10.1 to 1.10.2
* :pushpin: Automatic update of dependency methodtools from 0.1.0 to 0.1.1
* :pushpin: Automatic update of dependency boto3 from 1.10.0 to 1.10.1
* :pushpin: Automatic update of dependency boto3 from 1.9.253 to 1.10.0
* :pushpin: Automatic update of dependency thoth-python from 0.6.4 to 0.6.5
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.3 to 2.8.4
* :pushpin: Automatic update of dependency boto3 from 1.9.252 to 1.9.253
* :pushpin: Automatic update of dependency boto3 from 1.9.251 to 1.9.252
* :pushpin: Automatic update of dependency boto3 from 1.9.250 to 1.9.251
* :pushpin: Automatic update of dependency boto3 from 1.9.249 to 1.9.250
* :pushpin: Automatic update of dependency boto3 from 1.9.248 to 1.9.249
* :pushpin: Automatic update of dependency boto3 from 1.9.247 to 1.9.248
* :pushpin: Automatic update of dependency boto3 from 1.9.246 to 1.9.247
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.3 to 0.6.4
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.9 to 1.3.10
* :pushpin: Automatic update of dependency boto3 from 1.9.245 to 1.9.246
* :pushpin: Automatic update of dependency boto3 from 1.9.244 to 1.9.245
* :pushpin: Automatic update of dependency boto3 from 1.9.243 to 1.9.244
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* :pushpin: Automatic update of dependency pytest from 5.2.0 to 5.2.1
* :pushpin: Automatic update of dependency pytest-cov from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency boto3 from 1.9.242 to 1.9.243
* :pushpin: Automatic update of dependency pytest-cov from 2.7.1 to 2.8.0
* :pushpin: Automatic update of dependency boto3 from 1.9.241 to 1.9.242
* :pushpin: Automatic update of dependency boto3 from 1.9.240 to 1.9.241
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* :pushpin: Automatic update of dependency boto3 from 1.9.239 to 1.9.240
* :pushpin: Automatic update of dependency boto3 from 1.9.238 to 1.9.239
* :pushpin: Automatic update of dependency pytest from 5.1.3 to 5.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.237 to 1.9.238
* :pushpin: Automatic update of dependency boto3 from 1.9.236 to 1.9.237
* :pushpin: Automatic update of dependency boto3 from 1.9.235 to 1.9.236
* :pushpin: Automatic update of dependency alembic from 1.2.0 to 1.2.1
* :pushpin: Automatic update of dependency boto3 from 1.9.234 to 1.9.235
* :pushpin: Automatic update of dependency boto3 from 1.9.233 to 1.9.234
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency pytest from 5.1.2 to 5.1.3
* :pushpin: Automatic update of dependency boto3 from 1.9.232 to 1.9.233
* :pushpin: Automatic update of dependency alembic from 1.1.0 to 1.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.231 to 1.9.232
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency boto3 from 1.9.230 to 1.9.231
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* :pushpin: Automatic update of dependency boto3 from 1.9.229 to 1.9.230
* :pushpin: Automatic update of dependency thoth-python from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency pydgraph from 1.2.0 to 2.0.2
* :pushpin: Automatic update of dependency boto3 from 1.9.222 to 1.9.229
* :pushpin: Automatic update of dependency boto3 from 1.9.228 to 1.9.229
* :pushpin: Automatic update of dependency boto3 from 1.9.227 to 1.9.228
* :pushpin: Automatic update of dependency boto3 from 1.9.226 to 1.9.227
* :pushpin: Automatic update of dependency boto3 from 1.9.225 to 1.9.226
* :pushpin: Automatic update of dependency pydgraph from 2.0.1 to 2.0.2
* :pushpin: Automatic update of dependency boto3 from 1.9.224 to 1.9.225
* :pushpin: Automatic update of dependency boto3 from 1.9.223 to 1.9.224
* :pushpin: Automatic update of dependency pydgraph from 1.2.0 to 2.0.1
* :pushpin: Automatic update of dependency boto3 from 1.9.222 to 1.9.223
* :pushpin: Automatic update of dependency boto3 from 1.9.221 to 1.9.222
* :pushpin: Automatic update of dependency boto3 from 1.9.220 to 1.9.221
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.219 to 1.9.220
* :pushpin: Automatic update of dependency boto3 from 1.9.218 to 1.9.219
* :pushpin: Automatic update of dependency boto3 from 1.9.217 to 1.9.218
* :pushpin: Automatic update of dependency boto3 from 1.9.216 to 1.9.217
* :pushpin: Automatic update of dependency boto3 from 1.9.215 to 1.9.216
* :pushpin: Automatic update of dependency boto3 from 1.9.214 to 1.9.215
* :pushpin: Automatic update of dependency boto3 from 1.9.213 to 1.9.214
* :pushpin: Automatic update of dependency boto3 from 1.9.212 to 1.9.213
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.211 to 1.9.212
* :pushpin: Automatic update of dependency boto3 from 1.9.210 to 1.9.211
* :pushpin: Automatic update of dependency boto3 from 1.9.209 to 1.9.210
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* :pushpin: Automatic update of dependency boto3 from 1.9.208 to 1.9.209
* :pushpin: Automatic update of dependency boto3 from 1.9.207 to 1.9.208
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* :pushpin: Automatic update of dependency boto3 from 1.9.206 to 1.9.207
* :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* :pushpin: Automatic update of dependency voluptuous from 0.11.5 to 0.11.7
* :pushpin: Automatic update of dependency boto3 from 1.9.205 to 1.9.206
* :pushpin: Automatic update of dependency thoth-python from 0.6.0 to 0.6.1
* :pushpin: Automatic update of dependency boto3 from 1.9.204 to 1.9.205
* :pushpin: Automatic update of dependency boto3 from 1.9.203 to 1.9.204
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* :pushpin: Automatic update of dependency boto3 from 1.9.202 to 1.9.203
* :pushpin: Automatic update of dependency boto3 from 1.9.201 to 1.9.202
* :pushpin: Automatic update of dependency boto3 from 1.9.200 to 1.9.201
* :pushpin: Automatic update of dependency boto3 from 1.9.199 to 1.9.200
* :pushpin: Automatic update of dependency boto3 from 1.9.185 to 1.9.186
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* :pushpin: Automatic update of dependency boto3 from 1.9.184 to 1.9.185
* :pushpin: Automatic update of dependency boto3 from 1.9.183 to 1.9.184
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency boto3 from 1.9.182 to 1.9.183
* :pushpin: Automatic update of dependency boto3 from 1.9.181 to 1.9.182
* :pushpin: Automatic update of dependency boto3 from 1.9.180 to 1.9.181
* :pushpin: Automatic update of dependency moto from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency boto3 from 1.9.179 to 1.9.180
* :pushpin: Automatic update of dependency boto3 from 1.9.178 to 1.9.179
* :pushpin: Automatic update of dependency boto3 from 1.9.176 to 1.9.178
* :pushpin: Automatic update of dependency boto3 from 1.9.175 to 1.9.176
* :pushpin: Automatic update of dependency boto3 from 1.9.174 to 1.9.175
* :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency boto3 from 1.9.173 to 1.9.174
* :pushpin: Automatic update of dependency pydgraph from 1.1.2 to 1.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.172 to 1.9.173
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* :pushpin: Automatic update of dependency boto3 from 1.9.171 to 1.9.172
* :pushpin: Automatic update of dependency boto3 from 1.9.170 to 1.9.171
* :pushpin: Automatic update of dependency boto3 from 1.9.169 to 1.9.170
* :pushpin: Automatic update of dependency boto3 from 1.9.168 to 1.9.169
* :pushpin: Automatic update of dependency boto3 from 1.9.167 to 1.9.168
* :pushpin: Automatic update of dependency boto3 from 1.9.166 to 1.9.167
* :pushpin: Automatic update of dependency boto3 from 1.9.165 to 1.9.166
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* :pushpin: Automatic update of dependency boto3 from 1.9.164 to 1.9.165
* :pushpin: Automatic update of dependency pydgraph from 1.1.1 to 1.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.163 to 1.9.164
* :pushpin: Automatic update of dependency boto3 from 1.9.162 to 1.9.163
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency boto3 from 1.9.161 to 1.9.162
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency boto3 from 1.9.159 to 1.9.161
* :pushpin: Automatic update of dependency boto3 from 1.9.158 to 1.9.159
* :pushpin: Automatic update of dependency boto3 from 1.9.157 to 1.9.158
* :pushpin: Automatic update of dependency boto3 from 1.9.156 to 1.9.157
* :pushpin: Automatic update of dependency boto3 from 1.9.155 to 1.9.156
* :pushpin: Automatic update of dependency boto3 from 1.9.154 to 1.9.155
* :pushpin: Automatic update of dependency boto3 from 1.9.153 to 1.9.154
* :pushpin: Automatic update of dependency boto3 from 1.9.152 to 1.9.153
* :pushpin: Automatic update of dependency boto3 from 1.9.151 to 1.9.152
* :pushpin: Automatic update of dependency boto3 from 1.9.150 to 1.9.151
* :pushpin: Automatic update of dependency boto3 from 1.9.149 to 1.9.150
* :pushpin: Automatic update of dependency boto3 from 1.9.148 to 1.9.149
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency boto3 from 1.9.147 to 1.9.148
* :pushpin: Automatic update of dependency boto3 from 1.9.146 to 1.9.147
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* :pushpin: Automatic update of dependency boto3 from 1.9.145 to 1.9.146
* :pushpin: Automatic update of dependency amun from 0.2.0 to 0.2.1
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency boto3 from 1.9.144 to 1.9.145
* :pushpin: Automatic update of dependency boto3 from 1.9.143 to 1.9.144
* :pushpin: Automatic update of dependency boto3 from 1.9.142 to 1.9.143
* :pushpin: Automatic update of dependency boto3 from 1.9.141 to 1.9.142
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* :pushpin: Automatic update of dependency boto3 from 1.9.140 to 1.9.141
* :pushpin: Automatic update of dependency boto3 from 1.9.139 to 1.9.140
* :pushpin: Automatic update of dependency boto3 from 1.9.138 to 1.9.139
* :pushpin: Automatic update of dependency boto3 from 1.9.137 to 1.9.138
* :pushpin: Automatic update of dependency pydgraph from 1.1 to 1.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.136 to 1.9.137
* :pushpin: Automatic update of dependency boto3 from 1.9.135 to 1.9.136
* :pushpin: Automatic update of dependency boto3 from 1.9.134 to 1.9.135
* :pushpin: Automatic update of dependency moto from 1.3.7 to 1.3.8
* :pushpin: Automatic update of dependency pydgraph from 1.0.3 to 1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.130 to 1.9.134
* Automatic update of dependency boto3 from 1.9.98 to 1.9.101
* Automatic update of dependency boto3 from 1.9.84 to 1.9.91
* Automatic update of dependency pytest from 4.1.1 to 4.2.0
* Automatic update of dependency cython from 0.29.3 to 0.29.5
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Automatic update of dependency boto3 from 1.9.83 to 1.9.84
* Automatic update of dependency pytest from 4.0.2 to 4.1.1
* Automatic update of dependency boto3 from 1.9.73 to 1.9.83
* Automatic update of dependency cython from 0.29.2 to 0.29.3
* Automatic update of dependency uvloop from 0.11.3 to 0.12.0
* Automatic update of dependency pytest-cov from 2.6.0 to 2.6.1
* Automatic update of dependency flexmock from 0.10.2 to 0.10.3
* Automatic update of dependency boto3 from 1.9.71 to 1.9.73
* Automatic update of dependency boto3 from 1.9.67 to 1.9.71
* Automatic update of dependency boto3 from 1.9.66 to 1.9.67
* Automatic update of dependency boto3 from 1.9.65 to 1.9.66
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Automatic update of dependency cython from 0.29.1 to 0.29.2
* Automatic update of dependency boto3 from 1.9.64 to 1.9.65
* Automatic update of dependency boto3 from 1.9.63 to 1.9.64
* Automatic update of dependency thoth-common from 0.4.6 to 0.5.0
* Automatic update of dependency boto3 from 1.9.62 to 1.9.63
* Automatic update of dependency requests from 2.20.1 to 2.21.0
* Automatic update of dependency boto3 from 1.9.61 to 1.9.62
* Automatic update of dependency boto3 from 1.9.60 to 1.9.61
* Automatic update of dependency boto3 from 1.9.59 to 1.9.60
* Automatic update of dependency boto3 from 1.9.58 to 1.9.59
* Automatic update of dependency boto3 from 1.9.57 to 1.9.58
* Automatic update of dependency boto3 from 1.9.55 to 1.9.57
* Automatic update of dependency amun from 0.1.3 to 0.2.0
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency boto3 from 1.9.51 to 1.9.55
* Automatic update of dependency boto3 from 1.9.50 to 1.9.51
* Automatic update of dependency cython from 0.29 to 0.29.1
* Automatic update of dependency pytest from 4.0.0 to 4.0.1
* Automatic update of dependency boto3 from 1.9.49 to 1.9.50
* Automatic update of dependency boto3 from 1.9.48 to 1.9.49
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Automatic update of dependency boto3 from 1.9.47 to 1.9.48
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Automatic update of dependency boto3 from 1.9.46 to 1.9.47
* Automatic update of dependency pytest-timeout from 1.3.2 to 1.3.3
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Automatic update of dependency boto3 from 1.9.45 to 1.9.46
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1
* Automatic update of dependency boto3 from 1.9.44 to 1.9.45
* Automatic update of dependency pytest from 3.10.1 to 4.0.0
* Automatic update of dependency boto3 from 1.9.43 to 1.9.44
* Automatic update of dependency boto3 from 1.9.42 to 1.9.43
* Automatic update of dependency pytest from 3.10.0 to 3.10.1
* Automatic update of dependency boto3 from 1.9.41 to 1.9.42
* Automatic update of dependency boto3 from 1.9.40 to 1.9.41
* Automatic update of dependency requests from 2.20.0 to 2.20.1
* Automatic update of dependency boto3 from 1.9.39 to 1.9.40
* Automatic update of dependency boto3 from 1.9.38 to 1.9.39
* Automatic update of dependency boto3 from 1.9.37 to 1.9.38
* Automatic update of dependency moto from 1.3.6 to 1.3.7
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* Automatic update of dependency boto3 from 1.9.36 to 1.9.37
* Automatic update of dependency boto3 from 1.9.35 to 1.9.36
* Automatic update of dependency uvloop from 0.11.2 to 0.11.3
* Automatic update of dependency boto3 from 1.9.34 to 1.9.35
* Automatic update of dependency boto3 from 1.9.33 to 1.9.34
* Automatic update of dependency thoth-common from 0.3.15 to 0.3.16
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Automatic update of dependency pytest from 3.9.2 to 3.9.3
* Automatic update of dependency boto3 from 1.9.32 to 1.9.33
* Automatic update of dependency boto3 from 1.9.30 to 1.9.32
* Automatic update of dependency boto3 from 1.9.29 to 1.9.30
* Automatic update of dependency pytest from 3.9.1 to 3.9.2
* Automatic update of dependency boto3 from 1.9.28 to 1.9.29
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* Automatic update of dependency boto3 from 1.9.27 to 1.9.28
* Automatic update of dependency boto3 from 1.9.26 to 1.9.27
* Automatic update of dependency requests from 2.19.1 to 2.20.0
* Automatic update of dependency boto3 from 1.9.25 to 1.9.26
* Automatic update of dependency boto3 from 1.9.24 to 1.9.25
* Automatic update of dependency pytest from 3.8.2 to 3.9.1
* Automatic update of dependency boto3 from 1.9.23 to 1.9.24
* Automatic update of dependency cython from 0.28.5 to 0.29
* Automatic update of dependency boto3 from 1.9.22 to 1.9.23
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.11
* Automatic update of dependency boto3 from 1.9.21 to 1.9.22
* Automatic update of dependency boto3 from 1.9.19 to 1.9.21
* Automatic update of dependency boto3 from 1.9.16 to 1.9.19
* Automatic update of dependency pytest from 3.8.1 to 3.8.2
* Automatic update of dependency boto3 from 1.9.15 to 1.9.16
* Automatic update of dependency boto3 from 1.9.14 to 1.9.15
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Automatic update of dependency boto3 from 1.9.11 to 1.9.14
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Automatic update of dependency boto3 from 1.9.10 to 1.9.11
* Automatic update of dependency boto3 from 1.9.9 to 1.9.10
* Automatic update of dependency pytest from 3.7.3 to 3.8.1
* Automatic update of dependency boto3 from 1.8.3 to 1.9.9
* Automatic update of dependency pytest-cov from 2.5.1 to 2.6.0
* Automatic update of dependency thoth-common from 0.2.4 to 0.3.1
* Automatic update of dependency moto from 1.3.4 to 1.3.6
* Automatic update of dependency thoth-common from 0.2.3 to 0.2.4
* Automatic update of dependency boto3 from 1.8.2 to 1.8.3
* Automatic update of dependency thoth-common from 0.2.2 to 0.2.3
* Automatic update of dependency pytest-timeout from 1.3.1 to 1.3.2
* Automatic update of dependency boto3 from 1.8.1 to 1.8.2
* Automatic update of dependency pytest from 3.7.1 to 3.7.3
* Automatic update of dependency boto3 from 1.7.75 to 1.8.1
* Automatic update of dependency boto3 from 1.7.74 to 1.7.75
* Automatic update of dependency boto3 from 1.7.73 to 1.7.74
* Automatic update of dependency boto3 from 1.7.72 to 1.7.73
* Automatic update of dependency boto3 from 1.7.55 to 1.7.56
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.52 to 1.7.54
* Automatic update of dependency cython from 0.28.3 to 0.28.4
* Automatic update of dependency thoth-common from 0.1.0 to 0.2.0
* Automatic update of dependency boto3 from 1.7.51 to 1.7.52

## Release 0.29.1 (2020-11-23T17:20:14)
### Features
* result must be cast to list (#2114)
* Release of version 0.29.0 (#2113)
* Release of version 0.28.0 (#2112)
* add function to run amcheck and check for db corruption (#2105)
* Release of version 0.27.1 (#2103)
* Install thoth-ssdeep requirement for thoth-storages
* Release of version 0.27.0 (#2100)
* Changes in schema for bug, internal trigger and data analysis (#2046)
* Release of version 0.26.1 (#2090)
* Adjust DM sync (#2086)
* Release of version 0.26.0
* Provide a method for storing user requests (#2078)
* Release of version 0.25.17 (#2077)
* Match location where provenance-checker documents are stored (#2070)
* :sparkles: ignore more
* Release of version 0.25.16 (#2067)
* Adjust query filters (#2065)
* Adjust alembic migration (#2064)
* add error flag to si-sync (#2054)
* Fix cache handling and add ability to drop the cache (#2050)
* Release of version 0.25.15 (#2044)
* Adjust docstring (#2037)
* Release of version 0.25.14
* Correct queries after changes in schema (#2036)
* Added changes to kebechet model (#2024)
* Release of version 0.25.13 (#2032)
* Rename flag to be generalized (#2030)
* Release of version 0.25.12 (#2029)
* Adjust query for new flag is_downloadable (#2027)
* Correct docstring (#2025)
* add func for updating downloadable function (#2022)
* add flag for missing src distro (#2021)
* Release of version 0.25.11 (#2015)
* Adjust comment
* Adjust query for SI unanalyzed
* Add query to retrieve packages SI analyzed
* Adjust SI queries after schema change
* Invert order to allow sync (#2010)
* Release of version 0.25.10 (#2005)
* Fix sync for security (#2002)
* Release of version 0.25.9 (#2001)
* Remove package-analyzer related bits (#1994)
* Release of version 0.25.8 (#1993)
* Add queries for SI metrics
* Release of version 0.25.7 (#1986)
* Added query to get SI unanalyzed packages (#1963)
* Introduce query for document ids with solver error (#1976)
* :arrow_up: Relock the pipfile.lock
* Release of version 0.25.6
* query.all returns type List[result] not List[str]
* Release of version 0.25.5 (#1962)
* Add filters to method
* Release of version 0.25.4 (#1958)
* Propagate platform information in dependents query (#1954)
* Propagate platform when syncing revsolver results (#1955)
* Release of version 0.25.3 (#1953)
* Release of version 0.25.2 (#1946)
* Add information about heads on schema up2date check (#1917)
* Fix revsolver syncing logic (#1944)
* Release of version 0.25.1 (#1938)
* add cache and return None if empty (#1929)
* Add long_description_content_type (#1927)
* Release of version 0.25.0 (#1923)
* adding aggregated points to wrong location (#1919)
* Use postgres 10.12 in podman-compose as in the cluster (#1911)
* Release of version 0.24.5 (#1910)
* Use method from thoth-common (#1907)
* Release of version 0.24.4 (#1904)
* Map old domain to new (#1897)
* Release of version 0.24.3 (#1896)
* Sync inspections results (#1892)
* Do raise on counting, return zero instead (#1893)
* Release of version 0.24.2 (#1891)
* Release of version 0.24.1 (#1878)
* Adjust SI classes (#1881)
* Remove plural, only one build is done per inspection (#1880)
* Sync si aggregated (#1873)
* Fix missing normalize_os_version (#1868)
* Source type column (#1862)
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Update OWNERS
* Release of version 0.24.0
* Add import
* Add database
* Update .zuul.yaml
* Use variable only
* small change
* more messages
* Move imports of amun to local scope
* Introduce a method for checking if the given inspection exists
* Add missing exports of inspection adapters
* Implement adapters for inspections
* Maintain order
* Release of version 0.23.2
* Add import or classes cannot be accessed
* Remove parts moved to thoth-common
* Fix migration creating indexes
* Release of version 0.23.1
* Change class names and add them to __init__
* Release of version 0.23.0
* Add platform to the schema
* Perform schema version check only if the database is created
* added a 'tekton trigger tag_release pipeline issue'
* Release of version 0.22.12
* Changed function name
* removed is
* Added method to count active installations
* add is_missing flag to depends on query
* Release of version 0.22.11
* Added update to readme
* Docstring update
* Added activate deactivate functions
* Add is_missing optional argument to all pypackageversion queries
* Added is_active column
* Alembic file
* App columns not nullable
* Removed table constraints
* Changed order
* add new calling convention for flags/statements
* Updated alembic version
* Added kebhut table to models
* Release of version 0.22.10
* Add correct docstring
* Add query to count a table
* :pushpin: Automatic dependency re-locking
* Release of version 0.22.9
* Map ubi to rhel
* Release of version 0.22.8
* Adjust commit message
* Introduce get_dependents query
* Fix return value
* Use RHEL 8
* Release of version 0.22.7
* add assignments to query
* Release of version 0.22.6
* Consider also boolean values
* Optimize accessing dict
* Minor correction for package-update-api
* Consider also raw date without datetime in to_dict()
* Explictly cast datetime to a string
* Fix obtaining model attributes in model.to_dict()
* Correct README for graph-backup-job
* do not set query
* with_entities
* Join
* New alembic version
* Use Text everywhere
* Created query to retrieve adviser runs to be re run
* Move url filter inside if-if statement
* Do not delete rows, keep track of present hashes
* TODO
* Revert "API calls for package-update-consumer"
* Remove print
* Link Adviser Run with Python Package Versio Entity
* Release of version 0.22.5
* Release of version 0.22.4
* Reduce number of queries for environment markers by caching results
* Add arguments and doc string to remove hash
* upcase
* Add empty env template
* Function to remove missing hash from database
* reorder function arguments
* Remove typeshed dev dependency
* Update using subquery
* Add conventions and query template
* Add naming conventions docs for queries
* Specify condition for join
* Remove unecessary join
* Index url is in the pythonpackageindex table
* prepend AdviserRun to origin
* with ... as session
* Add self as postional argument
* Follow API naming conventions
* Fix database migration for python_package_version.is_missing
* Release of version 0.22.3
* Only get packages used by most recent advise
* Move import to local use
* Add distinct modifier for origin
* API calls for package-update-consumer
* Alembic update
* flag for missing package version
* Change regex expression
* Release of version 0.22.2
* Release of version 0.22.1
* All counts optional
* Include models using `fullmatch` instead of `search`
* Added option to exclude models from generated schema
* Update .thoth.yaml
* Release of version 0.22.0
* raise valueError
* Address issue #1573
* Avoid one join in the query
* Fix package symbols query
* Set default to False to reduce logging
* Fix inspection syncing for RHEL
* Fix OS name synced in container image analysis
* No need to query for package extract run - software environment can be directly used
* Alembic update
* Filter early
* outer join causing none values
* Refactor query for retrieving symbols in an image
* Make cuda version optional
* Simplified API functions
* Created query to monitor bloat data
* Fix method call to serialize models
* Fixed missing index issue
* Release of version 0.21.11
* Add missing keys to inspection schema validation
* new GitHub templates
* Added build log analysis result observations to graph database
* Release of version 0.21.10
* Make keys Optional
* Release of version 0.21.9
* Release of version 0.21.8
* Adjust parameter in query for PI
* Correct datatype
* Add missing key to sync inspections
* Set Packages Extract flag is_external to True always
* Missing change in query name to follow created standards
* Normalize OS version by discarding any minor release in RHEL release string
* Release of version 0.21.7
* Introduce a way to parametrize memory cache size
* Add index for solved table - it optimizes the has_solver_error query in adviser
* Release of version 0.21.6
* Release of version 0.21.5
* Alembic didn't create correct change in schema
* Release of version 0.21.4
* Consider only enabled indexes in unsolved queries
* Introduce a query for retrieving Python package entity names
* Release of version 0.21.3
* Release of version 0.21.2
* Release of version 0.21.1
* Fix parameter name for syncing provenance-checker documents
* Provide environment variable marker flag when retrieving transitive deps
* Correct inspection sync key
* Release of version 0.21.0
* Use datetime to sort results
* Fix advised software stack sync
* Format using black
* Drop id columns on relation tables
* Release of version 0.20.6
* Fix syncing external software environments coming from adviser
* Release of version 0.20.5
* Correct key from inspection output
* Missing randomize
* Adjust to follow naming convention
* Introduce software environment specific queries
* Release of version 0.20.4
* Release of version 0.20.3
* Fix syncs in versions
* Release of version 0.20.2
* Happy new year!
* Remove string size limitations from depends_on table
* Release of version 0.20.1
* :sparkles: added a PR template
* Fix keyword argument passing
* Release of version 0.20.0
* Do not show alembic info on configure_logger
* Super has no __del__
* Do not dispose engine in destructor
* Log number of dumps maintained
* Implement rotation of backups
* Fixes in reStructuredText in README file
* Release of version 0.19.30
* Release of version 0.19.29
* Increment solver error cache
* Increase cache for caching solver errors
* Remove unused indexes in depends_on table
* Fix Automatic Update Failure
* Sync cuda version
* Add missing filter
* Release of version 0.19.28
* Generalize function to retrieve multi values key metadata
* Add platforms
* WIP: Adjust Python Package Metadata query
* Add Thamos documentation
* Document automatic graph-backup job
* More formatting changes
* Minor docs reformatting
* Show database schema
* Provide is_s2i flag for adviser runs
* Point documentation to other libraries
* Add aggregated_at column to CVE
* Select distinct CVEs
* Adjust tests to new metadata
* Add deployment name to the result schema
* Release of version 0.19.27
* UBI:8 has optional variant_id
* Release of version 0.19.26
* Add Google Analytics
* Adjust testsuite
* Provide OS release schema
* Adjust default is_provided value
* Rename flag to is_provided_package_version
* Change Sphinx theme
* Correct staticmethod
* Release of version 0.19.25
* Increase characters metadata in keywords and summary metadata
* Optimize Analyzed Python Packages queries
* Optimnize unsolved queries
* Optimize queries
* Cache environment marker evaluation result
* :package: store database backup to ceph storage
* Fix Issue #1308 not iterable
* Fix alembic configuration instantiation issues
* Gather document id from document_id field
* :pushpin: Automatic dependency re-locking
* Use open instead of pathlib to adress PV in-cluster issues
* Make library thread safe
* Introduced sorting type in queries
* Fix wrong staticmethod
* Release of version 0.19.24
* Fix referencing store if is_local is set
* Add ability to sync documents based on absolute path
* Release of version 0.19.23
* Use context manager for handling sessions
* Fix warning for migration configuration check
* Release of version 0.19.22
* Correct output of queries
* Release of version 0.19.21
* Use same version as in the cluster
* Fix wrong rebase
* Dispose engine on disconnect
* Dispose engine on connect issues
* Release of version 0.19.20
* Use default pooling from sqlalchemy
* Adjust output query for metric
* Optimized/Improved query to retrieve unsolved Python Packages
* Fix schema check
* State ignoring a role assignment in docs
* Release of version 0.19.19
* Fix wrong propagation of is_local flag
* Increase character length for keywords metadata
* Release of version 0.19.18
* Correct attribute for metadata Provides-Extra
* Release of version 0.19.17
* Adjust sync for inspections
* Minor changes
* Release of version 0.19.16
* Pick metadata which were computed
* Grouped Metadata Distutils
* Created MetadataProvidesExtra
* Created MetadataProjectUrl
* Created MetadataRequiresExternal
* Created MetadataPlatform
* New models for PythonPackage Metadata that have multiple values
* Fix query to CVE for a given python package version entity
* Graph database cache has been removed
* Sync documents from a local directory if requested
* Release of version 0.19.15
* Randomize retrievals of unanalyzed Python packages
* Randomize retrieval of unsolved Python packages
* Correct errors for pytest
* Introduce enum classes for safe API
* Turn off checking thoth module by mypy
* Start using mypy in strict mode
* Fix retrieval of Python digests query
* Release of version 0.19.14
* Fix model for index url in the query
* Keep Python package tuples positional arguments
* Release of version 0.19.13
* Update naming queries according to Thoth convention
* Issue warning on connection to the database if schema is not up2date
* Update the schema
* Query to retrieve ML frameworks names
* Correct query to get metadata for Python Package
* HasArtifact is linked with PythonPackageVersionEntity table
* Revert "Symbol-API"
* Drop unique constraint in depends_on table
* added the registry to look for pgweb
* added podman-compose to dev packages list
* Fix model assignment when syncing results of Python interpreters
* Release of version 0.19.12
* Fixing the func argunment names
* consistency in using the variable force
* Fix index url issue, now properly
* Fix index_url key, now properly
* Fix version key dereference
* Fix index url key in new solvers implementation
* Release of version 0.19.11
* Handle issues in a better way
* Increase lines per file in Coala configuration
* Query environment markers stored in the database
* Add support for extras in the Python package dependencies retrieval query
* Introduce additional exception types for specific exceptions raised
* Drop cache support
* Updated .coafile to allow for longer files
* Coala errors
* More verbose errors, require all parameters
* Add offset and count
* Increase max lines per file
* Add api to get versioned symbols
* Get internal software & hardware environments
* Start using mypy for type checks
* Add missing provides-extra column to Python metadata
* Add missing columns to Python metadata
* Generic webhook updated to trigger the build from zuul
* Release of version 0.19.10
* Add update sync schema for PackageExtract
* Correct syncing issue
* Allow nullable software environemnts in the schema
* Fix multiple heads present
* Fix reference to variable in the query
* Fix query to retrieve number of unsolved packages
* Sync python interpreters
* Queries for packages with error in solvers and adjust schema
* Increase lenght file
* Added dependency monkey schema
* Added schema for package-extract sync
* Added solver sync schema
* Fix linkage of artifacts in Python package version entities
* Created adviser sync schema
* Add thoth sync schema for Amun
* Created docs for syncs inside Thoth Database
* Queries for packages with error in solvers and adjust schema
* Created solver functions following  naming convention
* Add missing import
* Remove unused import
* Created is_external for PackageExtractRun
* State how to implement syncing logic for any workload job done in the cluster
* Update syncs
* Changed schema and Added new Tables
* Update functions for metrics
* Add examples to docstrings
* Generate migration for new schema
* Convert function according to new naming convention
* Remove obsolete exception
* Expose sync_documents outside of module
* Implement a generic approach to sync any document
* Sync duration
* Generalized module varibale for count
* Created functions for get_python_packages cases
* Correct outputs
* New python_package_versions_count functions
* Hide query
* Added distinct flag
* New query
* get_python_package_version_count
* New queries for python packages
* Release of version 0.19.9
* Fix testsuite with recent changes
* Add duration to the result schema
* Release of version 0.19.8
* New query: count software stacks per type
* New queries
* Update queries
* Show an example run how to create a local PostgreSQL instance
* Use podman-compose
* Log what is being synced during graph syncs
* State graphviz package as a dependency when generating schema images
* Release of version 0.19.7
* Fix path to alembic versions - it has changed recently
* Allow limit latest versions to be None
* Make solver name optional when retrieving unsolved packages
* Introduce a check to verify the current database schema is up2date
* Drop also alembic version table
* Distribute alembic migrations with thoth-storages
* Release of version 0.19.6
* Add missing migrations to requirements.txt file
* Normalize Python package versions before each insert or query
* Make sure devs update to most recent version before generating new versions
* Make coala happy
* Use UTC when generating schema versions
* Generate initial schema using Alembic
* Start using Alembic for database migrations
* Add missing method used to register new packages in package releases
* Release of version 0.19.5
* Document how to dump and restore database in the running cluster
* Adjust logged message to inform about concurrent writes
* Randomize retrieval of unsolved Python packages
* Fix unsolved Python packages query
* Adjust signature of method to respect its return value
* Release of version 0.19.4
* Count and limit for advises can be nullable
* Increase advisory message for CVEs
* Release of version 0.19.3
* Disable connection pooling
* Release of version 0.19.2
* Update inspection sync for Upsert behaviour
* Implemented CASCADE on delete for Foreign Keys
* Release of version 0.19.1
* Release of version 0.19.0
* Remove accidentally committed file
* Add missing software stack relation to inspections
* Add missing import
* Disable cache inserts by default as they are expensive
* upsert-like logic
* Logic to sync inspection
* Increase lines allowed in a file
* Sync pacakge-analyzer results
* Sync system symbols detected by a package-extract
* Fix returned variable
* Check for solver errors before adding package to cache
* Start session with subtransactions enabled
* Be explicit about join
* Remove unique constraint
* Rewrite cache query to retrieved dependencies
* Raise NotFoundError if no records were found
* Implement method for listing analyses
* Implement method for getting analysis metadata
* Make methods which create data without starting transaction private
* Remove methods which should not be used outside of module
* Unify environment type handling
* Sync system symbols detected by a package-extract
* Reformat using black
* Introduce logic for syncing dependency-monkey documents
* Unify software stack creation handling
* Unify Python package version handling in PostgreSQL
* Move cache specific function to cache implementation
* Fix property name
* Introduce a new query which is used by adviser to filter out based on indexes
* Fix coala complains
* Remove old schema files
* Switch to PostgreSQL
* capture error
* Sync package analyzer error
* Add error flag to package analyzer run
* Remove index key
* Adjust tests to work with new implementation
* Do not raise exception, return None instead
* Call dgraph initialization
* Remove caching on top of Dgraph
* Remove accidentally committed file
* Mirror PostgreSQL with Dgraph for now
* PostgreSQL implementation
* Provide mechanism to clear in-memory cache
* Add entries to cache only if there were no solver errors
* Provide more information on cache statistics
* Use methodtools to properly handle lru cache on methods
* Use sqlite3 as cache
* Adjust query for retrieving transitive dependencies
* Adjust syncing logic to new depends_on schemantics
* Add is_provided flag
* Coala errors
* Store symbols
* Release of version 0.18.6
* Fix query for retrieving unsolved Python packages
* Minor changes to the function which returns unanalyzed packages
* Release of version 0.18.5
* Introduce a flag to retrieve only solved packages
* Use Python package name normalization from thoth-python module
* Release of version 0.18.4
* Fix Package Analyzer results syncing
* Fixes Syncing of Package Extract results
* Release of version 0.18.3
* Release of version 0.18.2
* Added missing inspection schema checks for voluptuous
* Release of version 0.18.1
* Solved conflict pinning to older version
* Corrected datatype-error for syncing
* Release of version 0.18.0
* New Dgraph function for PI
* Release of version 0.17.0
* Fix handling of pytest arguments in setup.py
* Revert changes in docker-compose
* Remove unused dependencies
* Rewrite querying logic for transitive dependencies retrieval
* Avoid copies when retrieving transitive dependencies
* Optimize retrieval of transitive queries
* Release of version 0.16.0
* Corrected voluptuous requirements for inspection schema:
* Modified Inspection schema
* Updated schema for PIConv
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
* Enable logging of graph database queries for debugging
* Fix handling of query filter
* Propagate OS information to runtime/buildtime environment nodes
* Update schema to capture os-release information
* Sync information about operating system captured in package-extract
* Update schema image respecting recent changes in PiMatmul
* Fix vertex cache handling
* Regenerate schema
* Add PythonFileDigest to schema documentation
* Introduce delete operation on top of models
* sync_package_analysis_documents
* Release of version 0.14.8
* Document schema hadnling in a living deployment
* Update dgraph.py
* Update README to show how to connect to the graph database from code
* Parametrize retrieval of unsolvable packages for the given solver
* Release of version 0.14.7
* Parametrize `@cascade` by `only_known_index` parameter
* Release of version 0.14.6
* Release of version 0.14.5
* Release of version 0.14.4
* Introduce retry exception on concurrent upsert writes
* :star: alphabetically order the files
* Release of version 0.14.3
* PackageAnalysisResultsStore is added
* Introduce pagination and solver_name filter
* Document local Dgraph instance setup
* Release of version 0.14.2
* Modified logic of the query to retrieve unsolved python packages for a given solver
* Update schema image for Thoth KG
* Update dgraph model schema for new parameters for PI
* Release of version 0.14.1
* Fix wrong variable reference
* Provide OS version and name as a string
* Release of version 0.14.0
* Ignore changelog file in coala, it's getting too large
* Release of version 0.13.0
* Release of version 0.12.0
* Removed unusued functions
* New UserHardwareInformation entity
* Update for Dgraph
* Check for cyclic dependencies in transitive query
* Fix number of overall results
* Qute fields as they are stored as strings
* Enhance exception information to give better information
* Release of version 0.11.4
* Fix normalization issue - normalize only package names
* An environment can have no analyses associated
* Release of version 0.11.3
* Provide method for buildtime environment listing
* Release of version 0.11.2
* Introduce mechanism to avoid gRPC issues when serializing large stacks
* Implement query for retrieving information about build-time errors
* Increase back-off count
* Implement back-off for random time in case of concurent upsert writes
* Release of version 0.11.1
* Fix computing edge hashes
* Created missing functions for Dgraph
* Normalize Python package names before inserting them into database
* Release of version 0.11.0
* Fix coala complains
* Implement query for retrieving transitive dependencies
* Fix python_sync_analysis
* Add missing provenance checker name
* Implement get_python_package_tuples for Dgraph
* Obsolete also unsolved_runtime_environments
* Remove obsolete queries
* Implemented get_all_versions_python_package method for Dgraph
* Add @normalize to flatten results
* Add @normalize to flatten results
* Add @normalize to flatten results
* Add normalization for package_name
* Added ecoystem filter
* Add Francesco to module authors
* Remove unused imports in dgraph.py implementation
* Implement query for retrieving artifact hashes from database
* Add query for checking provenance checker document id presence
* Implemment logic for checking if adviser run is present in db
* Fix query to retrieve solver count
* User software stack can have adviser or provenance-checker document id
* Implement query for retrieving image analysis count
* Implement query for retrieving solver error count
* Fix handling target UID for vertexes
* Implement runtime_environment_listing for Dgraph
* Retrieve read-only transaction for query operations
* Sync also digests when syncing solver documents
* Add missing annotations to models
* Remove checks which are already present in _create_python_package_record
* Fix syncing dependencies found in solver documents
* Schema proposal for Dgraph
* Add register_python_package_index to Dgraph implementation
* completed method for dgraph
* Introduce get_analysis_metadata for Dgraph
* Fix facets syntax when syncing edges dictionaries
* Implement get_python_package_index_urls for Dgraph
* Improve schema handling
* Switch to Dgraph
* Release of version 0.10.0
* New functions for janusgraph
* update schema file
* Fix coala complains
* Adjust method signatures
* Be consistent with return type, return always nan
* Update schema
* Error in query get_analyzer_documents_count()
* Add Thoth's configuration file
* Make runtime and buildtime environment names shared
* Release of version 0.9.7
* Use Sphinx for documentation
* Delete ceph.py.orig
* Fix solver error flag handling
* Add missing dot in Python version
* Respect errors in dependencies of packages
* Track solver_errors on depends_on edges
* Add missing ecosystem in query
* Remove duplicit definition
* black reformatted the file
* This repo requires Python 3.6
* Fix split count
* Fix solver name handling
* Add missing export from thoth.storages module
* Fix path to origin value of adviser and provenance-checker resutls
* Be consistent with property naming
* Update schema in docs
* Create relations between all the models in the graph database
* Introduce logic for syncing provenance check documents
* Adjust query to return unsolved packages for the given solver
* Update README with the most recent information about schema generation
* Increase number of lines per file
* Capture recommendation type in the graph model
* Introduce advised relationship
* Fix in markup
* State thoth-schema file path directly
* State automatic schema generation in README file
* Release of version 0.9.6
* Respect runtime environment in queries for direct dependencies
* Let callee preserve None values
* Consider hardware with no None values
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
* Depends on has to take account also environment
* Method can be static
* Adjust schema to reflect the current implementation
* Adjust solver related parts of schema for platform specifc features
* Provide method for solver name parsing
* Introduce flag exposing "existed" for Python package version
* Perform only graph or ceph sync if requested
* Move OpenShift specific bits to OpenShift
* Disconnect in destructor
* Avoid goblin model details in output
* Update README.rst
* Release of version 0.9.5
* Introduce name for a software stack
* Introduce query for querying software stacks
* Retrieve python package versions using asyncio
* ignoring some coala errors
* Reformat using black
* Do not handle exception twice
* Release of version 0.9.4
* Aggregate hashes from the graph database for the given package
* Performance index cannot be passed as None
* Fix query
* Version 0.9.3
* Include also requirements-test.txt in package
* Version 0.9.2
* Include requirements.txt when packaging
* Release of version 0.9.1
* Do not forget to install Amun for interaction with Amun
* Fixes for CI
* Consider index when retrieving transitive dependencies
* Include index url in the releases listing
* Release of version 0.9.0
* Corrected README file
* Introduce query for gathering sha256 hashes
* Hashes are positional argument
* Create digest entries in the graph database for python packages
* Add long description for PyPI
* Use index_url in the graph database
* Sync indexes into the graph database
* Update schema document
* Introduce has_artifact edge
* Artifact hashes in graph database
* Use base image name if there were not installed any native pkgs
* Report which inspection id is being synced
* Hardware can be even None
* Log about Amun results gathering
* Introduce graceful flag for inspection syncs
* Return directly list, not chain iterable
* Update schema in docs
* Do not forget to install Amun client
* Update schema docs
* Fix recent errors
* Fix errors
* Fix syntax error
* Be consistent with storage prefix naming
* Rename observation_document_id to inspection_document_id
* Introduce buildtime environment model
* Fix CI
* Fix CI
* Fix CI
* Adjust document_id gathering
* Introduce methods for checking documents based on id
* added a pyproject.toml to keep black happy
* using thoth's coala job
* using thoth-pytest job
* Fix pytest4 warning
* Update schema documentation
* Release of version 0.8.0
* Add a query to check for solved packages
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
* Release of version 0.7.4
* Fix unparseable solver result sync
* Release of version 0.7.3
* Correctly handle decorator wrappers
* Introduce dependency monkey reports adapter
* Fix query to retrieve all package versions
* Fix document naming
* Fix CI failures
* Rename error flags
* Introduce unparsed flag
* Introduce unparsed flag
* Keep schema up2date with recent schema changes
* Hostname is not equal to document id
* Introduce transitive dependencies gathering method
* Normalize names of packages that are inserted into graph database
* Release of version 0.7.2
* Introduce unsolvable flag
* Release of version 0.7.1
* Release of version 0.7.0
* Use job id as document id instead of pod id
* Implement image lookup for fast checks of image analyses
* Release of version 0.6.0
* Remove ignore comments
* Fix CI
* Add timestamp to the result schema
* Release of version 0.5.4
* Edge property is not a vertex property
* Release of version 0.5.3
* Update README file
* Introduce query for gathering dependencies
* Specify Python index from which the package came from
* Introduce check whether the given Python package exists
* Release of version 0.5.2
* Revert to the last release
* Revert "Release of version 0.5.6"
* Release of version 0.5.6
* Release of version 0.5.5
* Update .zuul.yaml
* Release of version 0.5.4
* Release of version 0.5.3
* Update janusgraph.py
* Sync debian packages to the graph database
* Release of version 0.5.2
* Revert "put it in zuul's user-api queue"
* put it in zuul's user-api queue
* change the queue
* change the queue
* Create adapter for provenance reports
* Release of version 0.5.1
* Store information about Python vulnerabilities
* Fix missing import
* added VSCode directory to git ignore list
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
* Initial dependency lock
* Delete Pipfile.lock for relocking dependencies
* Update .zuul.yaml
* removing pydocstyle
* preparing release 0.0.33
* removing unneeded E501
* Version 0.0.32
* Version 0.0.31
* added the gate pipeline to the core queue
* preparing for a zuul driven, fully coala compliant 0.0.30 release
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
* Ignore eggs in coala
* Run coala in non-interactive mode
* Make coala happy again
* Run coala in CI
* Version 0.0.26
* Test Ceph/S3 adapters against mocked environment
* Update .gitignore
* Tests for cache
* Be consistent with indentation
* Different botocore versions behave differently
* Tests for Ceph adapter
* Test result schema
* Correctly propagate connection check to Ceph adapter
* Provide a way to specify bucket prefix explicitly
* Create initial tests
* Introduce Ceph connection check
* Fix yarl issues
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
* Check for object existence
* Preperly return property value
* Use __properties__ instead of __dict__
* Fix missing self reference
* Version 0.0.21
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
* Introduce a function to find PyPI packages that deps were not resolved
* Add README file
* Version 0.0.18
* Version 0.0.17
* Provide routines to check solver results or analysis results presence
* Add spaces after equal sign
* Version range should be always stated
* Also state package name on depends_on edge
* Filter out irrelevant artifact requirements.txt from sync
* Version 0.0.16
* Fix wrong attribute reference
* Version 0.0.15
* Fix wrong property name
* Add missing attributes during sync
* Fix ecosystem name
* Be more sensitive with sync errors
* Fix missing argument
* Fix property types
* Bump schema docs version
* Update schema docs
* Revisit graph sync
* Version 0.0.14
* Remove nested .gitignore
* Respect changes in schema renaming
* Package version is now package_version
* Package version is now package_version
* Unify property naming
* Schema documentation
* Fix behavior in Jupyter notebooks to respect env variables
* Make caching configurable
* Implement cache handling
* Provide a way to specify source_id/target_id explicitly
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
* Version 0.0.7
* Add adapter for build logs
* Add method for iterating over results in Ceph
* Version 0.0.6
* Abstract document_id handling logic
* Abstract prefix creation
* Version 0.0.5
* Do not create bucket on Ceph for now
* Use RESULT_TYPE field to distinguish between database adapters
* Add missing dependnecy - boto3
* Require keyword arguments for constructor
* Create Ceph adapter
* State only direct requirements in requirements.txt
* Make the g object accessible for the graph access
* Use new create() methods to be consistent
* Version 0.0.4
* Rename JanusGraphDatabase to GraphDatabase
* Update requirements.txt
* Version 0.0.3
* Add forgotten dependency
* Version 0.0.2
* Version 0.0.1
* Add logic to iterate over available results
* State all packages in requirements file
* Do not check requirements hashes for now
* Fix docstring
* Add .gitignore
* Implement analysis results store adapter
* Implement solver results store adapter
* Implement disconnecting logic
* Create initial classes with interface
* Add .travis.yml configuration file
* Initial project import
### Bug Fixes
* Raise an exception when the given record was not found (#2069)
* Alembic timeline fix (#2035)
* Fix logging error when database schema is not up2date (#1949)
* Default platform if not available in the solver document (#1901)
* Update lock file to fix issues in CI
* fixed re-active
* fixed typo and changed migrations
* pytest failing due to hash mismatch
* Corrected wrong keys used in solver sync
* Relock to fix sqlalchemy release hashes
* join with PythonSoftware not external
* Add check in sync when report is not provided by Adviser
* Sync missing packages if adviser failed due to unknown dependencies
* normalize, distinct, fix index
* Adjust syncing logic of Dependency Monkey documents based on the current output
* Fix wrong argument name propagated
* Do not sync package errors if the given package is not provided
* Optimized Solved quries with error
* Issue warning instead of error
* Fix bug in checking for dist key
* Relax fatal error on syncing unmatched metadata
* Issue warning if the database schema is not initialized yet in connect
* Fix error when case 3 is not declared yet
* Raise not found error if the given Python index is not found
* Minor fix to address typo
* Minor typo fixes in README file
* Minor fixes to make dependency monkey syncs work properly
* Fix invalid foreign key error on schema creation
* Use indexes and minor fixes
* Retrieve packages that are not analyzed by Package-Analyzer
* Fix key error 'python'
* Quote user input parts of the query in error message produced
* Check if the given package in the given version was solved by specific solver
* Provide better exception message on parsing error
* Fix wrong indentation in adviser results sync
* Minor fix to display correct release in title of docs html
* Fix missing import causing issues in graph-sync-job
* Return None if no entity was found for in query_one
* Fix issues reported by coala runs
* Remove failing test
* Reformat using black, fix some coala warnings
* fix one check
* Fixed output after tests
* Minor code fixes
* Turn ram size into float to fix serialization/deserialization issues
* Adjust query to track solver errors on the given runtime env
* fixing some coala errors
* Introduce adviser error flag in user stack
* If adviser analysis was not succesfull no lockfile is provided
* Minor fixes in method signatures
* Linter fixes
* Do not query graph database if no id is provided
* Fix key error if hardware was not provided on Amun
* fixed some coala problems
* fixing project.post.jobs.trigger-build.vars.webhook_url
* using envvar that are injected by OpenShift to discover janusgraph servcie host and port, this requires that a service called "janusgraph" is created
* fixed line too long
* some pytest fixed wrt the prefix
* some pylint fixed
* Modify requirements to fix yarl issues
* Skip mercator errors that are not stored anyway
* Improve error handling
* Fix issue with vertex property being stored instead of its value
* Revisit key error fix
* A temporary fix for mercator result being None
* Fix key error when syncing to graph database
* Log exception instead of error
* Log exception instead of error
* Fix error when syncing data to janusgraph with VertexProperty
* Fix wrong model name
* Fix wrong parameter
* Raise appropriate exception on non-existing key
* Raise an exception on invalid schema
### Improvements
* check for cuda nvcc and found in file version (#2092)
* :arrow_down: removed the files as they are no longer required
* change flag name and alembic commands (#2033)
* Add query for adviser run per source type (#1997)
* Make package version and package index optional in get_depends_on (#1975)
* State how to install podman and podman-compose (#1971)
* Introduce method for retrieving inspection ids and count (#1879)
* Create queries for SI retrieval for certain package name, version , index (#1882)
* make coala happy
* No inspection result batch size
* Reproduce methods specific for postgres
* Adjust methods
* more info
* Fix computing batch size of inspection jobs
* break security indicators into two stores
* Add routines and index for platform manipulation
* create class for storing security indicators
* Fix typo
* Raise NotFoundError if setting is_missing flag for non-existing package
* docstring match variable name
* function for checking current availability of package
* Adjust method name based on review comment
* Add logic for syncing revsolver result
* Small typo
* Modified logic for adviser sync
* Modify schema and logic to sync adviser run
* Update storages function to be more versatile and follow conventions
* Remove unnecessary imports
* Add doc strings and remove unnecessary subtransactions
* Python must have major and minor version
* Fix index creation for symbols queries
* Change from externalsoftware environment, and uncouple id index
* Move cache to storage level
* Add indexes to improve abi queries
* Fix reference to variable
* added some files to gitignore
* :sweat_smile: Auto pip and black formatting
* Create index for has_artifact table
* Adjust index for PPV combinations
* Fix query for enabled index
* Query for index_url before creating index
* Adjust datatype for conv PI to sync inspection results
* Do not use id when counting tables
* Create index for CVE step to omit sequence scan
* correct typo
* Sync package version requested rather than package version reported
* Optimize marker evaluation result query for adviser
* Adjust names of parameters to respect their semantics
* Introduce PyBench PI table and adjust sync logic for inspection
* Make some log info optional
* Create index for get_depends_on query
* Adjust tests to the new implementation
* Remove self to make method static
* Introduce ping method
* :green_heart: added more builds that need to be triggered
* Standardize sync logic entries for Adviser, Provenance Checker and Dependency Monkey
* Added MetadataDistutils, updated sync logic, schema docs, Tested syncs
* Created MetadataRequiresDist and MetadataSupportedPlatform
* Cache some of the query results
* Remove old pydgraph dependency
* Add normalization for package_name and package_version
* Standardize and unify query for python artifact hashes
* State maintainer and project url in setup.py
* Sync container image size
* Fixing the func argunment design
* Introduce query for checking marker evaluation results
* Remove graph cache tests
* Fix signature of the private method - unsolved edge cases
* Created query for python package metadata for user-api
* Created and updated queries for analyzed packages
* New schema and sync in Solver for PythonPackageMetadata
* Consistenly sync index_url and package_version
* Added schema for package extract
* Added provenance checker sync and all components sync
* Updated and tested all solved/unsolved functions
* Remove old file for Dgraph related tests
* Add logic for syncing marker and extra
* No NULL values for some PythonPackageVersion attributes
* We use psql not pg_restore
* Fix small typo
* New class methods for InspectionStore
* Provide method for disabling and enabling Python package index
* Remove unused imports
* State how to print stats to logs in README file
* Log statistics of graph cache and memory cache if requested so
* Use more generic env variable names
* Add tests and adjust existing testsuite to respect cache flags
* Updates for consistency
* Fix cache test
* Remove debug warnings accidentally committed
* Package version can have some of the values None
* Remove unused parameters
* Implement logic for syncing adviser results
* Fix typos
* Implement logic for syncing provenance checker results
* Implement logic for syncing package-extract results
* updated schema
* Add statistics of queries to sqlite3 cache
* Optimize two queries into one and iterate over all configurations resolved
* Do not use slots as LRU cache wrappers fail
* Provide adapter for storing and restoring graph cache in builds
* Introduce cache for caching results of well-used packages
* Provide method for counting number of unsolved Python packages
* Add models for versioned symbols and associated edges
* Add PI for Conv1D and Conv2D for tensorflow
* Remove old test
* sync package analyzer results
* Update schema to include package analyzer
* State in the README file how to debug graph database queries
* Fix typo in matrix
* Add standard project template and code owners
* Rename models and properties
* Fix refactoring typo
* Introduce method for creating Python package version entities
* :dizzy: updated adapters for storing buillog analysis results and cache
* Require non-null `index_url` and `package_name`
* New tests for inspection schema check before sync
* code-style and new functions
* New sync logic for PI
* Update schema, functions and design schema
* Correct typo
* Reorganize Python package creation
* Remove unused method
* Implemented runtime_environment_analyses_listing method for Dgraph
* Implemented retrieve_unsolved_pypi_packages method for Dgraph
* Implemented retrieve_dependent_packages method for Dgraph
* Implemented retrieve_solved_pypi_packages method for Dgraph
* Implemented retrieve_unsolvable_pypi_packages method for Dgraph
* Fix typos
* Implemented retrieve_unparsable_pypi_packages method for Dgraph
* Implemented get_all_python_package_version_hashes_sha256 method for Dgraph
* Implemented python_package_exists method for Dgraph
* Implemented python_package_version_exists method for Dgraph
* Implemented get_python_packages_for_index method for Dgraph
* Implemented get_python_packages method for Dgraph
* Implemented analysis_records_exist method for Dgraph
* Implemented solver_records_exist method for Dgraph
* Fix get_analysis_metadata function, sync_functions, models and graph schema
* Implement method for gathering CVEs for Python packages
* Add query for checking presence of inspection runs
* Implement logic for querying for DependencyMonkey document presence
* Implement logic for checking image analysis run presence
* Fix query for checking solver document presence
* minor change
* Implemented get_all_python_packages_count method for Dgraph
* Introduce solver_document_id_exist method for Dgraph
* Fix sync of edge sync - source and target should not be part of sync
* New Edge between PythonPackageVersion and PythonPackageIndex
* Distinguish between runtime and buildtime environment
* Remove duplicit method
* Fix clash of runtime environment - model versus representing class
* Add type to queries to hit index
* :bug: removed the trailing slash
* Fix coala warnings
* this part of the path is no longer required
* Add CVE name when querying for CVEs
* Add python version and cuda version to graph schema
* Introduce adapter for storing caching analysis ids based on image digest
* Introduce method for gathering packages known to thoth based on index
* Do not rely in Gremlin queries for order of received items
* Fix typo in retrieve_dependencies(...) query
* Remove unused imports
* Assign index to all packages in inspection sync
* Normalize python package names before every graph operation
* Add index url to the check for Python package version existance
* Update README to include test suite in setup.py
* Use models to_dict method to obtain values
* Fix Python package index URL retrieval
* Add method for retrieving Python package index URLs
* Introduce method for registering Python package indexes
* Introduce method for syncing inspection documents
* Remove runtime and buildtime observations
* Create method for syncing inspections into janusgraph
* Do not use schema for inspections
* Remove unused variable
* Introduce sync methods
* Introduce adapter for inspection results
* Return also python package index model
* Introduce method for creating Python package index vertex
* Add python package index entity
* Add method for counting documents
* Add methods in janusgraph for metrics
* Exclude test directory
* Introduce methods for checking unsolvable and unparsed packages
* Introduce method for gathering python package versions
* Introduce observation models and adapter
* Fix variable name
* Change in variable names
* Run tests in Travis CI
* Add test dependencies
* Fix assertion test
* Abstract common code to a base class
* No need to copy env variables
* Add base class for tests
* Implement tests for build logs adapter
* Expose adapter for adviser results
* Introduce adapter for adviser for recommendations
* Introduce to_pretty_dict() method
* Introduce logic that wraps PyPI package creation
* Make sure we use correct attributes
* Log correct variable
* Use VertexProperty class for Vertex properties
* Initial schema creation and graph sync
* Reuse logic from result store base adapter in solver result adapter
* Reuse logic in analysis adapter from result base adapter
* Create result base for storing raw results onto Ceph
* Add base classes for vertex and edges to cover common logic
* Fix typo
* Create storage base class
* Add result schema for analyzer results
* Add docstrings for result store methods.
* Improve logging + refactor defaults
* Implement graph storing logic for JanusGraph
### Non-functional
* Add security and performance database enums (#1940)
* Drop methods tools to gain performance
* Adjust model performance for inspection output
* Fix performance indicator name
* Fix documentation for performance indicators
* Drop performance related query
* Adjust query for retrieving performance indicators
* Count number of performance indicators based on framework
* Introduce method for counting performance indicator entries
* Do not maintain schema for performance indicators
* Substitute from_properties with get_or_create in performance models
* Update schema based on updates to performance indicators
* Unify schema for creating performance indicators and their handling
* Use index for int values of performance indicators
* Always return float when computing average performance
* Implement method for gathering average performance
* Adjust performance query to respect runtime environment
* Extend performance query so it is more generic
* Improve handling of performance index
* Sync also performance index to janusgraph
* Introduce query for computing performance index
* Gather performance index from inspection jobs
* Rename failure test case for better readability
* Improving Goblin's driver performance
### Other
* remove variables
* remove imports
* remove sqlalchemy utils
* Remove duplicate entry
* Fix wrong base class
* Do not duplicate logic
* Use coala for code checks
* Refactor code to export defaults
### Automatic Updates
* :pushpin: Automatic update of dependency boto3 from 1.16.12 to 1.16.15 (#2089)
* :pushpin: Automatic update of dependency boto3 from 1.16.11 to 1.16.12 (#2087)
* :pushpin: Automatic update of dependency boto3 from 1.16.10 to 1.16.11 (#2082)
* :pushpin: Automatic update of dependency boto3 from 1.16.10 to 1.16.11 (#2081)
* :pushpin: Automatic update of dependency boto3 from 1.16.9 to 1.16.10 (#2076)
* :pushpin: Automatic update of dependency boto3 from 1.16.8 to 1.16.9
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#2062)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#2061)
* :pushpin: Automatic update of dependency boto3 from 1.16.6 to 1.16.8 (#2060)
* :pushpin: Automatic update of dependency boto3 from 1.16.0 to 1.16.6 (#2057)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#2056)
* :pushpin: Automatic update of dependency boto3 from 1.15.16 to 1.16.0 (#2055)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#2053)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#2052)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.19 to 1.3.20 (#2051)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1
* :pushpin: Automatic update of dependency boto3 from 1.15.11 to 1.15.16
* :pushpin: Automatic update of dependency boto3 from 1.15.9 to 1.15.11 (#2043)
* :pushpin: Automatic update of dependency boto3 from 1.15.8 to 1.15.9 (#2041)
* :pushpin: Automatic update of dependency boto3 from 1.15.7 to 1.15.8 (#2034)
* :pushpin: Automatic update of dependency boto3 from 1.15.6 to 1.15.7 (#2026)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#2023)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#2020)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#2019)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#2018)
* :pushpin: Automatic update of dependency boto3 from 1.15.1 to 1.15.6 (#2017)
* :pushpin: Automatic update of dependency voluptuous from 0.11.7 to 0.12.0 (#2011)
* :pushpin: Automatic update of dependency boto3 from 1.14.63 to 1.15.1 (#2012)
* :pushpin: Automatic update of dependency boto3 from 1.14.62 to 1.14.63 (#2009)
* :pushpin: Automatic update of dependency boto3 from 1.14.61 to 1.14.62 (#2006)
* :pushpin: Automatic update of dependency boto3 from 1.14.61 to 1.14.62 (#2004)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#1996)
* :pushpin: Automatic update of dependency thoth-common from 0.18.2 to 0.19.0 (#1999)
* :pushpin: Automatic update of dependency boto3 from 1.14.60 to 1.14.61 (#1998)
* :pushpin: Automatic update of dependency alembic from 1.4.2 to 1.4.3 (#1991)
* :pushpin: Automatic update of dependency alembic from 1.4.2 to 1.4.3 (#1990)
* :pushpin: Automatic update of dependency thoth-common from 0.18.1 to 0.18.2 (#1989)
* :pushpin: Automatic update of dependency boto3 from 1.14.58 to 1.14.60 (#1988)
* :pushpin: Automatic update of dependency thoth-common from 0.18.0 to 0.18.1 (#1983)
* :pushpin: Automatic update of dependency thoth-common from 0.17.3 to 0.18.0 (#1982)
* :pushpin: Automatic update of dependency boto3 from 1.14.57 to 1.14.58 (#1981)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.2 (#1973)
* :pushpin: Automatic update of dependency boto3 from 1.14.49 to 1.14.53 (#1972)
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#1970)
* :pushpin: Automatic update of dependency boto3 from 1.14.47 to 1.14.49 (#1969)
* :pushpin: Automatic update of dependency boto3 from 1.14.46 to 1.14.47 (#1956)
* :pushpin: Automatic update of dependency boto3 from 1.14.45 to 1.14.46 (#1950)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.18 to 1.3.19 (#1943)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#1942)
* :pushpin: Automatic update of dependency boto3 from 1.14.43 to 1.14.45 (#1941)
* :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#1935)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#1934)
* :pushpin: Automatic update of dependency pytest from 6.0.0 to 6.0.1 (#1933)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#1932)
* :pushpin: Automatic update of dependency boto3 from 1.14.31 to 1.14.43 (#1931)
* :pushpin: Automatic update of dependency thoth-common from 0.15.0 to 0.16.0 (#1924)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0 (#1921)
* :pushpin: Automatic update of dependency boto3 from 1.14.30 to 1.14.31 (#1920)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.15.0 (#1915)
* :pushpin: Automatic update of dependency boto3 from 1.14.28 to 1.14.30 (#1914)
* :pushpin: Automatic update of dependency boto3 from 1.14.26 to 1.14.28 (#1912)
* :pushpin: Automatic update of dependency boto3 from 1.14.22 to 1.14.26 (#1908)
* :pushpin: Automatic update of dependency boto3 from 1.14.21 to 1.14.22 (#1903)
* :pushpin: Automatic update of dependency pytest-timeout from 1.4.1 to 1.4.2 (#1900)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#1899)
* :pushpin: Automatic update of dependency boto3 from 1.14.19 to 1.14.21 (#1898)
* :pushpin: Automatic update of dependency boto3 from 1.14.18 to 1.14.19 (#1894)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.7 to 0.36.8 (#1889)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.7 to 0.36.8 (#1887)
* :pushpin: Automatic update of dependency boto3 from 1.14.17 to 1.14.18 (#1886)
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.6 to 0.36.7 (#1876)
* :pushpin: Automatic update of dependency thoth-common from 0.14.0 to 0.14.1 (#1875)
* :pushpin: Automatic update of dependency boto3 from 1.14.14 to 1.14.17 (#1874)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.0 (#1872)
* :pushpin: Automatic update of dependency boto3 from 1.14.13 to 1.14.14 (#1866)
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13 (#1865)
* :pushpin: Automatic update of dependency boto3 from 1.14.9 to 1.14.13 (#1864)
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.17 to 1.3.18
* :pushpin: Automatic update of dependency boto3 from 1.14.4 to 1.14.9
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.11 to 0.13.12
* :pushpin: Automatic update of dependency boto3 from 1.13.24 to 1.14.1
* :pushpin: Automatic update of dependency boto3 from 1.13.23 to 1.13.24
* :pushpin: Automatic update of dependency boto3 from 1.13.22 to 1.13.23
* :pushpin: Automatic update of dependency boto3 from 1.13.21 to 1.13.22
* :pushpin: Automatic update of dependency boto3 from 1.13.20 to 1.13.21
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* :pushpin: Automatic update of dependency boto3 from 1.13.19 to 1.13.20
* :pushpin: Automatic update of dependency boto3 from 1.13.18 to 1.13.19
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency boto3 from 1.13.17 to 1.13.18
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency boto3 from 1.13.16 to 1.13.17
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.5 to 0.36.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency boto3 from 1.13.15 to 1.13.16
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency boto3 from 1.13.14 to 1.13.15
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.13 to 1.13.14
* :pushpin: Automatic update of dependency boto3 from 1.13.12 to 1.13.13
* :pushpin: Automatic update of dependency boto3 from 1.13.11 to 1.13.12
* :pushpin: Automatic update of dependency boto3 from 1.13.10 to 1.13.11
* :pushpin: Automatic update of dependency boto3 from 1.13.6 to 1.13.9
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.16 to 1.3.17
* :pushpin: Automatic update of dependency boto3 from 1.13.5 to 1.13.6
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic update of dependency boto3 from 1.13.4 to 1.13.5
* :pushpin: Automatic update of dependency boto3 from 1.13.3 to 1.13.4
* :pushpin: Automatic update of dependency boto3 from 1.13.2 to 1.13.3
* :pushpin: Automatic update of dependency boto3 from 1.12.47 to 1.12.49
* :pushpin: Automatic update of dependency click from 7.1.1 to 7.1.2
* :pushpin: Automatic update of dependency boto3 from 1.12.46 to 1.12.47
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* :pushpin: Automatic update of dependency boto3 from 1.12.43 to 1.12.46
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* :pushpin: Automatic update of dependency boto3 from 1.12.38 to 1.12.39
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.15 to 1.3.16
* :pushpin: Automatic update of dependency boto3 from 1.12.37 to 1.12.38
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* :pushpin: Automatic update of dependency boto3 from 1.12.36 to 1.12.37
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.4 to 2.8.5
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.0 to 0.6.1
* :pushpin: Automatic update of dependency boto3 from 1.12.35 to 1.12.36
* :pushpin: Automatic update of dependency boto3 from 1.12.34 to 1.12.35
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency boto3 from 1.12.33 to 1.12.34
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.12.4 to 0.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.32 to 1.12.33
* :pushpin: Automatic update of dependency boto3 from 1.12.31 to 1.12.32
* :pushpin: Automatic update of dependency boto3 from 1.12.30 to 1.12.31
* :pushpin: Automatic update of dependency thoth-common from 0.12.3 to 0.12.4
* :pushpin: Automatic update of dependency boto3 from 1.12.29 to 1.12.30
* :pushpin: Automatic update of dependency thoth-common from 0.12.2 to 0.12.3
* :pushpin: Automatic update of dependency pyyaml from 5.3.1 to 3.13
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.28 to 1.12.29
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.1
* :pushpin: Automatic update of dependency boto3 from 1.12.27 to 1.12.28
* :pushpin: Automatic update of dependency pyyaml from 3.13 to 5.3.1
* :pushpin: Automatic update of dependency boto3 from 1.12.26 to 1.12.27
* :pushpin: Automatic update of dependency boto3 from 1.12.25 to 1.12.26
* :pushpin: Automatic update of dependency alembic from 1.4.1 to 1.4.2
* :pushpin: Automatic update of dependency boto3 from 1.12.24 to 1.12.25
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* :pushpin: Automatic update of dependency boto3 from 1.12.23 to 1.12.24
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.2 to 0.36.3
* :pushpin: Automatic update of dependency boto3 from 1.12.22 to 1.12.23
* :pushpin: Automatic update of dependency boto3 from 1.12.21 to 1.12.22
* :pushpin: Automatic update of dependency pytest from 5.3.5 to 5.4.1
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.1 to 0.36.2
* :pushpin: Automatic update of dependency pytest-mypy from 0.5.0 to 0.6.0
* :pushpin: Automatic update of dependency boto3 from 1.12.20 to 1.12.21
* :pushpin: Automatic update of dependency pyyaml from 5.3 to 3.13
* :pushpin: Automatic update of dependency boto3 from 1.12.19 to 1.12.20
* :pushpin: Automatic update of dependency boto3 from 1.12.18 to 1.12.19
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.14 to 1.3.15
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.13 to 1.3.14
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* :pushpin: Automatic update of dependency click from 7.0 to 7.1.1
* :pushpin: Automatic update of dependency boto3 from 1.12.16 to 1.12.18
* :pushpin: Automatic update of dependency boto3 from 1.12.10 to 1.12.11
* :pushpin: Automatic update of dependency boto3 from 1.12.9 to 1.12.10
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* :pushpin: Automatic update of dependency boto3 from 1.12.8 to 1.12.9
* :pushpin: Automatic update of dependency boto3 from 1.12.7 to 1.12.8
* :pushpin: Automatic update of dependency boto3 from 1.12.6 to 1.12.7
* :pushpin: Automatic update of dependency amun from 0.4.0 to 0.4.3
* :pushpin: Automatic update of dependency boto3 from 1.12.5 to 1.12.6
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.2 to 0.5.0
* :pushpin: Automatic update of dependency boto3 from 1.12.4 to 1.12.5
* :pushpin: Automatic update of dependency boto3 from 1.12.3 to 1.12.4
* :pushpin: Automatic update of dependency boto3 from 1.12.2 to 1.12.3
* :pushpin: Automatic update of dependency amun from 0.3.8 to 0.4.0
* :pushpin: Automatic update of dependency boto3 from 1.12.1 to 1.12.2
* :pushpin: Automatic update of dependency boto3 from 1.12.0 to 1.12.1
* :pushpin: Automatic update of dependency boto3 from 1.11.17 to 1.12.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency boto3 from 1.11.16 to 1.11.17
* :pushpin: Automatic update of dependency boto3 from 1.11.15 to 1.11.16
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* :pushpin: Automatic update of dependency boto3 from 1.11.14 to 1.11.15
* :pushpin: Automatic update of dependency boto3 from 1.11.13 to 1.11.14
* :pushpin: Automatic update of dependency boto3 from 1.11.12 to 1.11.13
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency boto3 from 1.11.11 to 1.11.12
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic update of dependency boto3 from 1.11.10 to 1.11.11
* :pushpin: Automatic update of dependency alembic from 1.3.3 to 1.4.0
* :pushpin: Automatic update of dependency boto3 from 1.11.9 to 1.11.10
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* :pushpin: Automatic update of dependency amun from 0.3.7 to 0.3.8
* :pushpin: Automatic update of dependency amun from 0.3.6 to 0.3.7
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency amun from 0.3.5 to 0.3.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* :pushpin: Automatic update of dependency boto3 from 1.11.8 to 1.11.9
* :pushpin: Automatic update of dependency boto3 from 1.11.7 to 1.11.8
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.12 to 1.3.13
* :pushpin: Automatic update of dependency alembic from 1.3.2 to 1.3.3
* :pushpin: Automatic update of dependency boto3 from 1.11.6 to 1.11.7
* :pushpin: Automatic update of dependency amun from 0.3.4 to 0.3.5
* :pushpin: Automatic update of dependency amun from 0.3.3 to 0.3.4
* :pushpin: Automatic update of dependency boto3 from 1.11.5 to 1.11.6
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* :pushpin: Automatic update of dependency boto3 from 1.11.4 to 1.11.5
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency amun from 0.3.2 to 0.3.3
* :pushpin: Automatic update of dependency boto3 from 1.11.3 to 1.11.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.28
* :pushpin: Automatic update of dependency amun from 0.3.1 to 0.3.2
* :pushpin: Automatic update of dependency boto3 from 1.11.2 to 1.11.3
* :pushpin: Automatic update of dependency boto3 from 1.11.1 to 1.11.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* :pushpin: Automatic update of dependency boto3 from 1.11.0 to 1.11.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* :pushpin: Automatic update of dependency amun from 0.3.0 to 0.3.1
* :pushpin: Automatic update of dependency boto3 from 1.10.50 to 1.11.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* :pushpin: Automatic update of dependency amun from 0.2.7 to 0.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.49 to 1.10.50
* :pushpin: Automatic update of dependency thoth-python from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency boto3 from 1.10.48 to 1.10.49
* :pushpin: Automatic update of dependency thoth-python from 0.8.0 to 0.9.0
* :pushpin: Automatic update of dependency boto3 from 1.10.47 to 1.10.48
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* :pushpin: Automatic update of dependency thoth-python from 0.7.1 to 0.8.0
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.3 to 1.3.4
* :pushpin: Automatic update of dependency pyyaml from 5.2 to 5.3
* :pushpin: Automatic update of dependency boto3 from 1.10.46 to 1.10.47
* :pushpin: Automatic update of dependency boto3 from 1.10.45 to 1.10.46
* :pushpin: Automatic update of dependency boto3 from 1.10.44 to 1.10.45
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.36.0 to 0.36.1
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency boto3 from 1.10.43 to 1.10.44
* :pushpin: Automatic update of dependency boto3 from 1.10.42 to 1.10.43
* :pushpin: Automatic update of dependency boto3 from 1.10.41 to 1.10.42
* :pushpin: Automatic update of dependency boto3 from 1.10.40 to 1.10.41
* :pushpin: Automatic update of dependency alembic from 1.3.1 to 1.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.39 to 1.10.40
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.11 to 1.3.12
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency boto3 from 1.10.38 to 1.10.39
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency boto3 from 1.10.35 to 1.10.38
* :pushpin: Automatic update of dependency boto3 from 1.10.34 to 1.10.35
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.35.0 to 0.36.0
* :pushpin: Automatic update of dependency boto3 from 1.10.33 to 1.10.34
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency boto3 from 1.10.32 to 1.10.33
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* :pushpin: Automatic update of dependency boto3 from 1.10.31 to 1.10.32
* :pushpin: Automatic update of dependency boto3 from 1.10.30 to 1.10.31
* :pushpin: Automatic update of dependency boto3 from 1.10.29 to 1.10.30
* :pushpin: Automatic update of dependency pyyaml from 5.1.2 to 5.2
* :pushpin: Automatic update of dependency boto3 from 1.10.28 to 1.10.29
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.19
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* :pushpin: Automatic update of dependency boto3 from 1.10.26 to 1.10.27
* :pushpin: Automatic update of dependency sqlalchemy-stubs from 0.2 to 0.3
* :pushpin: Automatic update of dependency boto3 from 1.10.25 to 1.10.26
* :pushpin: Automatic update of dependency boto3 from 1.10.24 to 1.10.25
* :pushpin: Automatic update of dependency boto3 from 1.10.23 to 1.10.24
* :pushpin: Automatic update of dependency boto3 from 1.10.22 to 1.10.23
* :pushpin: Automatic update of dependency boto3 from 1.10.21 to 1.10.22
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.20 to 1.10.21
* :pushpin: Automatic update of dependency boto3 from 1.10.19 to 1.10.20
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* :pushpin: Automatic update of dependency boto3 from 1.10.18 to 1.10.19
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency boto3 from 1.10.17 to 1.10.18
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* :pushpin: Automatic update of dependency boto3 from 1.10.16 to 1.10.17
* :pushpin: Automatic update of dependency alembic from 1.3.0 to 1.3.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* :pushpin: Automatic update of dependency boto3 from 1.10.15 to 1.10.16
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.10 to 1.3.11
* :pushpin: Automatic update of dependency boto3 from 1.10.14 to 1.10.15
* :pushpin: Automatic update of dependency boto3 from 1.10.13 to 1.10.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.5 to 0.7.1
* :pushpin: Automatic update of dependency boto3 from 1.10.12 to 1.10.13
* :pushpin: Automatic update of dependency boto3 from 1.10.11 to 1.10.12
* :pushpin: Automatic update of dependency boto3 from 1.10.10 to 1.10.11
* :pushpin: Automatic update of dependency boto3 from 1.10.9 to 1.10.10
* :pushpin: Automatic update of dependency python-dateutil from 2.8.1 to 2.8.0
* :pushpin: Automatic update of dependency boto3 from 1.10.8 to 1.10.9
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.1 to 0.4.2
* :pushpin: Automatic update of dependency python-dateutil from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency boto3 from 1.10.7 to 1.10.8
* :pushpin: Automatic update of dependency sqlalchemy-utils from 0.34.2 to 0.35.0
* :pushpin: Automatic update of dependency boto3 from 1.10.6 to 1.10.7
* :pushpin: Automatic update of dependency alembic from 1.2.1 to 1.3.0
* :pushpin: Automatic update of dependency boto3 from 1.10.5 to 1.10.6
* :pushpin: Automatic update of dependency boto3 from 1.10.4 to 1.10.5
* :pushpin: Automatic update of dependency boto3 from 1.10.3 to 1.10.4
* :pushpin: Automatic update of dependency boto3 from 1.10.2 to 1.10.3
* :pushpin: Automatic update of dependency methodtools from 0.1.1 to 0.1.2
* :pushpin: Automatic update of dependency pytest from 5.2.1 to 5.2.2
* :pushpin: Automatic update of dependency boto3 from 1.10.1 to 1.10.2
* :pushpin: Automatic update of dependency methodtools from 0.1.0 to 0.1.1
* :pushpin: Automatic update of dependency boto3 from 1.10.0 to 1.10.1
* :pushpin: Automatic update of dependency boto3 from 1.9.253 to 1.10.0
* :pushpin: Automatic update of dependency thoth-python from 0.6.4 to 0.6.5
* :pushpin: Automatic update of dependency psycopg2-binary from 2.8.3 to 2.8.4
* :pushpin: Automatic update of dependency boto3 from 1.9.252 to 1.9.253
* :pushpin: Automatic update of dependency boto3 from 1.9.251 to 1.9.252
* :pushpin: Automatic update of dependency boto3 from 1.9.250 to 1.9.251
* :pushpin: Automatic update of dependency boto3 from 1.9.249 to 1.9.250
* :pushpin: Automatic update of dependency boto3 from 1.9.248 to 1.9.249
* :pushpin: Automatic update of dependency boto3 from 1.9.247 to 1.9.248
* :pushpin: Automatic update of dependency boto3 from 1.9.246 to 1.9.247
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.3 to 0.6.4
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.9 to 1.3.10
* :pushpin: Automatic update of dependency boto3 from 1.9.245 to 1.9.246
* :pushpin: Automatic update of dependency boto3 from 1.9.244 to 1.9.245
* :pushpin: Automatic update of dependency boto3 from 1.9.243 to 1.9.244
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* :pushpin: Automatic update of dependency pytest from 5.2.0 to 5.2.1
* :pushpin: Automatic update of dependency pytest-cov from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency sqlalchemy from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency boto3 from 1.9.242 to 1.9.243
* :pushpin: Automatic update of dependency pytest-cov from 2.7.1 to 2.8.0
* :pushpin: Automatic update of dependency boto3 from 1.9.241 to 1.9.242
* :pushpin: Automatic update of dependency boto3 from 1.9.240 to 1.9.241
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* :pushpin: Automatic update of dependency boto3 from 1.9.239 to 1.9.240
* :pushpin: Automatic update of dependency boto3 from 1.9.238 to 1.9.239
* :pushpin: Automatic update of dependency pytest from 5.1.3 to 5.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.237 to 1.9.238
* :pushpin: Automatic update of dependency boto3 from 1.9.236 to 1.9.237
* :pushpin: Automatic update of dependency boto3 from 1.9.235 to 1.9.236
* :pushpin: Automatic update of dependency alembic from 1.2.0 to 1.2.1
* :pushpin: Automatic update of dependency boto3 from 1.9.234 to 1.9.235
* :pushpin: Automatic update of dependency boto3 from 1.9.233 to 1.9.234
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency pytest from 5.1.2 to 5.1.3
* :pushpin: Automatic update of dependency boto3 from 1.9.232 to 1.9.233
* :pushpin: Automatic update of dependency alembic from 1.1.0 to 1.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.231 to 1.9.232
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency boto3 from 1.9.230 to 1.9.231
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* :pushpin: Automatic update of dependency boto3 from 1.9.229 to 1.9.230
* :pushpin: Automatic update of dependency thoth-python from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency pydgraph from 1.2.0 to 2.0.2
* :pushpin: Automatic update of dependency boto3 from 1.9.222 to 1.9.229
* :pushpin: Automatic update of dependency boto3 from 1.9.228 to 1.9.229
* :pushpin: Automatic update of dependency boto3 from 1.9.227 to 1.9.228
* :pushpin: Automatic update of dependency boto3 from 1.9.226 to 1.9.227
* :pushpin: Automatic update of dependency boto3 from 1.9.225 to 1.9.226
* :pushpin: Automatic update of dependency pydgraph from 2.0.1 to 2.0.2
* :pushpin: Automatic update of dependency boto3 from 1.9.224 to 1.9.225
* :pushpin: Automatic update of dependency boto3 from 1.9.223 to 1.9.224
* :pushpin: Automatic update of dependency pydgraph from 1.2.0 to 2.0.1
* :pushpin: Automatic update of dependency boto3 from 1.9.222 to 1.9.223
* :pushpin: Automatic update of dependency boto3 from 1.9.221 to 1.9.222
* :pushpin: Automatic update of dependency boto3 from 1.9.220 to 1.9.221
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.219 to 1.9.220
* :pushpin: Automatic update of dependency boto3 from 1.9.218 to 1.9.219
* :pushpin: Automatic update of dependency boto3 from 1.9.217 to 1.9.218
* :pushpin: Automatic update of dependency boto3 from 1.9.216 to 1.9.217
* :pushpin: Automatic update of dependency boto3 from 1.9.215 to 1.9.216
* :pushpin: Automatic update of dependency boto3 from 1.9.214 to 1.9.215
* :pushpin: Automatic update of dependency boto3 from 1.9.213 to 1.9.214
* :pushpin: Automatic update of dependency boto3 from 1.9.212 to 1.9.213
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.211 to 1.9.212
* :pushpin: Automatic update of dependency boto3 from 1.9.210 to 1.9.211
* :pushpin: Automatic update of dependency boto3 from 1.9.209 to 1.9.210
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* :pushpin: Automatic update of dependency boto3 from 1.9.208 to 1.9.209
* :pushpin: Automatic update of dependency boto3 from 1.9.207 to 1.9.208
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* :pushpin: Automatic update of dependency boto3 from 1.9.206 to 1.9.207
* :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* :pushpin: Automatic update of dependency voluptuous from 0.11.5 to 0.11.7
* :pushpin: Automatic update of dependency boto3 from 1.9.205 to 1.9.206
* :pushpin: Automatic update of dependency thoth-python from 0.6.0 to 0.6.1
* :pushpin: Automatic update of dependency boto3 from 1.9.204 to 1.9.205
* :pushpin: Automatic update of dependency boto3 from 1.9.203 to 1.9.204
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* :pushpin: Automatic update of dependency boto3 from 1.9.202 to 1.9.203
* :pushpin: Automatic update of dependency boto3 from 1.9.201 to 1.9.202
* :pushpin: Automatic update of dependency boto3 from 1.9.200 to 1.9.201
* :pushpin: Automatic update of dependency boto3 from 1.9.199 to 1.9.200
* :pushpin: Automatic update of dependency boto3 from 1.9.185 to 1.9.186
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* :pushpin: Automatic update of dependency boto3 from 1.9.184 to 1.9.185
* :pushpin: Automatic update of dependency boto3 from 1.9.183 to 1.9.184
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency boto3 from 1.9.182 to 1.9.183
* :pushpin: Automatic update of dependency boto3 from 1.9.181 to 1.9.182
* :pushpin: Automatic update of dependency boto3 from 1.9.180 to 1.9.181
* :pushpin: Automatic update of dependency moto from 1.3.8 to 1.3.9
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency boto3 from 1.9.179 to 1.9.180
* :pushpin: Automatic update of dependency boto3 from 1.9.178 to 1.9.179
* :pushpin: Automatic update of dependency boto3 from 1.9.176 to 1.9.178
* :pushpin: Automatic update of dependency boto3 from 1.9.175 to 1.9.176
* :pushpin: Automatic update of dependency boto3 from 1.9.174 to 1.9.175
* :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency boto3 from 1.9.173 to 1.9.174
* :pushpin: Automatic update of dependency pydgraph from 1.1.2 to 1.2.0
* :pushpin: Automatic update of dependency boto3 from 1.9.172 to 1.9.173
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* :pushpin: Automatic update of dependency boto3 from 1.9.171 to 1.9.172
* :pushpin: Automatic update of dependency boto3 from 1.9.170 to 1.9.171
* :pushpin: Automatic update of dependency boto3 from 1.9.169 to 1.9.170
* :pushpin: Automatic update of dependency boto3 from 1.9.168 to 1.9.169
* :pushpin: Automatic update of dependency boto3 from 1.9.167 to 1.9.168
* :pushpin: Automatic update of dependency boto3 from 1.9.166 to 1.9.167
* :pushpin: Automatic update of dependency boto3 from 1.9.165 to 1.9.166
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* :pushpin: Automatic update of dependency boto3 from 1.9.164 to 1.9.165
* :pushpin: Automatic update of dependency pydgraph from 1.1.1 to 1.1.2
* :pushpin: Automatic update of dependency boto3 from 1.9.163 to 1.9.164
* :pushpin: Automatic update of dependency boto3 from 1.9.162 to 1.9.163
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency boto3 from 1.9.161 to 1.9.162
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency boto3 from 1.9.159 to 1.9.161
* :pushpin: Automatic update of dependency boto3 from 1.9.158 to 1.9.159
* :pushpin: Automatic update of dependency boto3 from 1.9.157 to 1.9.158
* :pushpin: Automatic update of dependency boto3 from 1.9.156 to 1.9.157
* :pushpin: Automatic update of dependency boto3 from 1.9.155 to 1.9.156
* :pushpin: Automatic update of dependency boto3 from 1.9.154 to 1.9.155
* :pushpin: Automatic update of dependency boto3 from 1.9.153 to 1.9.154
* :pushpin: Automatic update of dependency boto3 from 1.9.152 to 1.9.153
* :pushpin: Automatic update of dependency boto3 from 1.9.151 to 1.9.152
* :pushpin: Automatic update of dependency boto3 from 1.9.150 to 1.9.151
* :pushpin: Automatic update of dependency boto3 from 1.9.149 to 1.9.150
* :pushpin: Automatic update of dependency boto3 from 1.9.148 to 1.9.149
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency boto3 from 1.9.147 to 1.9.148
* :pushpin: Automatic update of dependency boto3 from 1.9.146 to 1.9.147
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* :pushpin: Automatic update of dependency boto3 from 1.9.145 to 1.9.146
* :pushpin: Automatic update of dependency amun from 0.2.0 to 0.2.1
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency boto3 from 1.9.144 to 1.9.145
* :pushpin: Automatic update of dependency boto3 from 1.9.143 to 1.9.144
* :pushpin: Automatic update of dependency boto3 from 1.9.142 to 1.9.143
* :pushpin: Automatic update of dependency boto3 from 1.9.141 to 1.9.142
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* :pushpin: Automatic update of dependency boto3 from 1.9.140 to 1.9.141
* :pushpin: Automatic update of dependency boto3 from 1.9.139 to 1.9.140
* :pushpin: Automatic update of dependency boto3 from 1.9.138 to 1.9.139
* :pushpin: Automatic update of dependency boto3 from 1.9.137 to 1.9.138
* :pushpin: Automatic update of dependency pydgraph from 1.1 to 1.1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.136 to 1.9.137
* :pushpin: Automatic update of dependency boto3 from 1.9.135 to 1.9.136
* :pushpin: Automatic update of dependency boto3 from 1.9.134 to 1.9.135
* :pushpin: Automatic update of dependency moto from 1.3.7 to 1.3.8
* :pushpin: Automatic update of dependency pydgraph from 1.0.3 to 1.1
* :pushpin: Automatic update of dependency boto3 from 1.9.130 to 1.9.134
* Automatic update of dependency boto3 from 1.9.98 to 1.9.101
* Automatic update of dependency boto3 from 1.9.84 to 1.9.91
* Automatic update of dependency pytest from 4.1.1 to 4.2.0
* Automatic update of dependency cython from 0.29.3 to 0.29.5
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Automatic update of dependency boto3 from 1.9.83 to 1.9.84
* Automatic update of dependency pytest from 4.0.2 to 4.1.1
* Automatic update of dependency boto3 from 1.9.73 to 1.9.83
* Automatic update of dependency cython from 0.29.2 to 0.29.3
* Automatic update of dependency uvloop from 0.11.3 to 0.12.0
* Automatic update of dependency pytest-cov from 2.6.0 to 2.6.1
* Automatic update of dependency flexmock from 0.10.2 to 0.10.3
* Automatic update of dependency boto3 from 1.9.71 to 1.9.73
* Automatic update of dependency boto3 from 1.9.67 to 1.9.71
* Automatic update of dependency boto3 from 1.9.66 to 1.9.67
* Automatic update of dependency boto3 from 1.9.65 to 1.9.66
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Automatic update of dependency cython from 0.29.1 to 0.29.2
* Automatic update of dependency boto3 from 1.9.64 to 1.9.65
* Automatic update of dependency boto3 from 1.9.63 to 1.9.64
* Automatic update of dependency thoth-common from 0.4.6 to 0.5.0
* Automatic update of dependency boto3 from 1.9.62 to 1.9.63
* Automatic update of dependency requests from 2.20.1 to 2.21.0
* Automatic update of dependency boto3 from 1.9.61 to 1.9.62
* Automatic update of dependency boto3 from 1.9.60 to 1.9.61
* Automatic update of dependency boto3 from 1.9.59 to 1.9.60
* Automatic update of dependency boto3 from 1.9.58 to 1.9.59
* Automatic update of dependency boto3 from 1.9.57 to 1.9.58
* Automatic update of dependency boto3 from 1.9.55 to 1.9.57
* Automatic update of dependency amun from 0.1.3 to 0.2.0
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency boto3 from 1.9.51 to 1.9.55
* Automatic update of dependency boto3 from 1.9.50 to 1.9.51
* Automatic update of dependency cython from 0.29 to 0.29.1
* Automatic update of dependency pytest from 4.0.0 to 4.0.1
* Automatic update of dependency boto3 from 1.9.49 to 1.9.50
* Automatic update of dependency boto3 from 1.9.48 to 1.9.49
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Automatic update of dependency boto3 from 1.9.47 to 1.9.48
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Automatic update of dependency boto3 from 1.9.46 to 1.9.47
* Automatic update of dependency pytest-timeout from 1.3.2 to 1.3.3
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Automatic update of dependency boto3 from 1.9.45 to 1.9.46
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1
* Automatic update of dependency boto3 from 1.9.44 to 1.9.45
* Automatic update of dependency pytest from 3.10.1 to 4.0.0
* Automatic update of dependency boto3 from 1.9.43 to 1.9.44
* Automatic update of dependency boto3 from 1.9.42 to 1.9.43
* Automatic update of dependency pytest from 3.10.0 to 3.10.1
* Automatic update of dependency boto3 from 1.9.41 to 1.9.42
* Automatic update of dependency boto3 from 1.9.40 to 1.9.41
* Automatic update of dependency requests from 2.20.0 to 2.20.1
* Automatic update of dependency boto3 from 1.9.39 to 1.9.40
* Automatic update of dependency boto3 from 1.9.38 to 1.9.39
* Automatic update of dependency boto3 from 1.9.37 to 1.9.38
* Automatic update of dependency moto from 1.3.6 to 1.3.7
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* Automatic update of dependency boto3 from 1.9.36 to 1.9.37
* Automatic update of dependency boto3 from 1.9.35 to 1.9.36
* Automatic update of dependency uvloop from 0.11.2 to 0.11.3
* Automatic update of dependency boto3 from 1.9.34 to 1.9.35
* Automatic update of dependency boto3 from 1.9.33 to 1.9.34
* Automatic update of dependency thoth-common from 0.3.15 to 0.3.16
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Automatic update of dependency pytest from 3.9.2 to 3.9.3
* Automatic update of dependency boto3 from 1.9.32 to 1.9.33
* Automatic update of dependency boto3 from 1.9.30 to 1.9.32
* Automatic update of dependency boto3 from 1.9.29 to 1.9.30
* Automatic update of dependency pytest from 3.9.1 to 3.9.2
* Automatic update of dependency boto3 from 1.9.28 to 1.9.29
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* Automatic update of dependency boto3 from 1.9.27 to 1.9.28
* Automatic update of dependency boto3 from 1.9.26 to 1.9.27
* Automatic update of dependency requests from 2.19.1 to 2.20.0
* Automatic update of dependency boto3 from 1.9.25 to 1.9.26
* Automatic update of dependency boto3 from 1.9.24 to 1.9.25
* Automatic update of dependency pytest from 3.8.2 to 3.9.1
* Automatic update of dependency boto3 from 1.9.23 to 1.9.24
* Automatic update of dependency cython from 0.28.5 to 0.29
* Automatic update of dependency boto3 from 1.9.22 to 1.9.23
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.11
* Automatic update of dependency boto3 from 1.9.21 to 1.9.22
* Automatic update of dependency boto3 from 1.9.19 to 1.9.21
* Automatic update of dependency boto3 from 1.9.16 to 1.9.19
* Automatic update of dependency pytest from 3.8.1 to 3.8.2
* Automatic update of dependency boto3 from 1.9.15 to 1.9.16
* Automatic update of dependency boto3 from 1.9.14 to 1.9.15
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Automatic update of dependency boto3 from 1.9.11 to 1.9.14
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Automatic update of dependency boto3 from 1.9.10 to 1.9.11
* Automatic update of dependency boto3 from 1.9.9 to 1.9.10
* Automatic update of dependency pytest from 3.7.3 to 3.8.1
* Automatic update of dependency boto3 from 1.8.3 to 1.9.9
* Automatic update of dependency pytest-cov from 2.5.1 to 2.6.0
* Automatic update of dependency thoth-common from 0.2.4 to 0.3.1
* Automatic update of dependency moto from 1.3.4 to 1.3.6
* Automatic update of dependency thoth-common from 0.2.3 to 0.2.4
* Automatic update of dependency boto3 from 1.8.2 to 1.8.3
* Automatic update of dependency thoth-common from 0.2.2 to 0.2.3
* Automatic update of dependency pytest-timeout from 1.3.1 to 1.3.2
* Automatic update of dependency boto3 from 1.8.1 to 1.8.2
* Automatic update of dependency pytest from 3.7.1 to 3.7.3
* Automatic update of dependency boto3 from 1.7.75 to 1.8.1
* Automatic update of dependency boto3 from 1.7.74 to 1.7.75
* Automatic update of dependency boto3 from 1.7.73 to 1.7.74
* Automatic update of dependency boto3 from 1.7.72 to 1.7.73
* Automatic update of dependency boto3 from 1.7.55 to 1.7.56
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.54 to 1.7.55
* Automatic update of dependency boto3 from 1.7.52 to 1.7.54
* Automatic update of dependency cython from 0.28.3 to 0.28.4
* Automatic update of dependency thoth-common from 0.1.0 to 0.2.0
* Automatic update of dependency boto3 from 1.7.51 to 1.7.52

## Release 0.29.2 (2020-12-01T18:31:02)
### Features
* Adjust constraint
* Update readme
* substitute new parameter
* Make parameter public
* bump python version (#2121)

## Release 0.29.3 (2020-12-04T13:47:42)
### Features
* Use sort() (#2137)

## Release 0.29.4 (2020-12-08T09:56:00)
### Features
* Use sort() correctly (#2144)
* Use proper naming convention of type 6 (#2141)
* included issue template to release missing module

## Release 0.30.0 (2021-01-04T10:34:25)
### Features
* Adjust docstring
* Change return val to be lst of repos, add example docstring
* Change return value
* Rename according to conventions, add .all(), change docstring
* Add get active installations method
### Improvements
* Add get_origin_count_per_source_type method
* Change method name to follow convention type 7

## Release 0.30.1 (2021-01-07T15:35:31)
### Features
* Correct-output (#2158)
* Filter out stored requests from listing (#2155)
* Remove coala from requirements (#2154)
### Bug Fixes
* Filter active installations in DB and fix method signature (#2156)

## Release 0.31.0 (2021-01-12T10:50:28)
### Features
* Add prefix for buildlog documents (#2164)
* :arrow_up: Automatic update of dependencies by kebechet. (#2166)
* :arrow_up: Automatic update of dependencies by kebechet. (#2163)
* Introduce queries to retrieve specifc document ids according to parameters (#2160)
### Improvements
* Normalization functions have been moved to common (#2153)

## Release 0.32.0 (2021-01-14T15:50:09)
### Features
* Add flters for solver query to retrieve document ids by error (#2171)
* Provide adapter for manipulating with parsed build logs (#2170)
### Improvements
* removed bissenbay, thanks for your contributions!

## Release 0.33.0 (2021-01-19T15:57:38)
### Features
* :arrow_up: Automatic update of dependencies by kebechet. (#2178)
* :arrow_up: Automatic update of dependencies by kebechet. (#2177)
* Refactor method for schema check (#2176)
* :arrow_up: Automatic update of dependencies by kebechet. (#2175)

## Release 0.34.0 (2021-02-01T10:05:32)
### Features
* Introduce queries to query Thoth s2i container images (#2201)
* :arrow_up: Automatic update of dependencies by kebechet. (#2200)
* :arrow_up: Automatic update of dependencies by kebechet. (#2198)
* Create query for querying Thoth's s2i container image symbols
* Sync s2i specific attributes to the right table
* Move Thoth s2i specific env vars to software environment models
* Sync Thoth specific environment variables from package-extract runs (#2192)
* :arrow_up: Automatic update of dependencies by kebechet. (#2190)
* :arrow_up: Automatic update of dependencies by kebechet. (#2186)
* :arrow_up: Automatic update of dependencies by kebechet. (#2184)
* remove call to install amcheck on postgres (#2183)
* :arrow_up: Automatic update of dependencies by kebechet. (#2182)
### Bug Fixes
* Do not sync Dependency Monkey document if any error is reported (#2187)
### Improvements
* Add migration for index
* Create index for Thoth's s2i base image attributes

## Release 0.35.0 (2021-02-02T21:49:44)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#2208)
* Fix sync solver (#2207)
### Bug Fixes
* Add queries and fix bug discovered (#2197)
### Improvements
* Create methods for manipulating with hardware environments (#2204)

## Release 0.35.1 (2021-02-03T07:22:44)
### Bug Fixes
* fix: the arguments for the normalize_os_version function

## Release 0.36.0 (2021-02-03T11:18:01)
### Features
* Merge queries to maintain consistency
* Adjust after review
* Adjust query for user software stack
* Sync unresolved from provenance checker report

## Release 0.37.0 (2021-02-15T10:52:58)
### Features
* Create an adapter for persisting requests to Dependency Monkey
* :arrow_up: Automatic update of dependencies by Kebechet (#2214)
* add marker file PEP561

## Release 0.38.0 (2021-03-04T19:54:36)
### Features
* Introduce a query for obtaining database size
* Add query for number of rows in alembic table
* update with pip, piplock, and .thoth.config dicts (#2227)
* :arrow_up: Automatic update of dependencies by Kebechet (#2225)

## Release 0.39.0 (2021-03-10T08:58:17)
### Features
* Add filters filtering based on image name
* Store information about images produced by AICoE CI on sync
* Add information about container images stored in env variables
* :arrow_up: Automatic update of dependencies by Kebechet (#2236)
* :arrow_up: Automatic update of dependencies by Kebechet (#2233)

## Release 0.39.1 (2021-03-12T21:03:49)
### Features
* Do not enforce Python version being set for non-external images (#2244)
* :arrow_up: Automatic update of dependencies by Kebechet (#2243)
* :arrow_up: Automatic update of dependencies by Kebechet (#2237)

## Release 0.39.2 (2021-03-16T20:55:30)
### Features
* Pin down sqlalchmey to be less than 1.4.0 version (#2255)
* :arrow_up: Automatic update of dependencies by Kebechet (#2253)
* :arrow_up: Automatic update of dependencies by Kebechet (#2249)
* :arrow_up: Automatic update of dependencies by Kebechet (#2246)
* remove goern as an approve
* Introduce pre-commit checks for storages (#2248)

## Release 0.39.3 (2021-03-19T17:54:19)
### Other
* Fix/avoid duplicate heads (#2258)

## Release 0.40.0 (2021-04-09T11:08:37)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#2278)
* Query results on Ceph based on date (#2277)
* :arrow_up: Automatic update of dependencies by Kebechet (#2276)
* :arrow_up: Automatic update of dependencies by Kebechet (#2274)
* :arrow_up: Automatic update of dependencies by Kebechet (#2271)
* :arrow_up: Automatic update of dependencies by Kebechet (#2268)
* :arrow_up: Automatic update of dependencies by Kebechet (#2262)
### Improvements
* Minor improvements in docs (#2275)
* Create index for depends_on considering is_missing and extras (#2263)

## Release 0.41.0 (2021-04-28T13:01:54)
### Features
* Provide ability to include end_date in the results listing (#2283)
* :arrow_up: Automatic update of dependencies by Kebechet (#2287)
* :arrow_up: Automatic update of dependencies by Kebechet (#2284)
* Add check for same date supplied for date iteration
### Improvements
* Extend methods to handle requests (#2286)
* Remove unused comment (#2285)

## Release 0.42.0 (2021-05-03T07:05:48)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#2294)
* Provide methods for deleting data from the database (#2292)
* :arrow_up: Automatic update of dependencies by Kebechet (#2290)

## Release 0.43.0 (2021-06-01T19:04:08)
### Features
* Reorder imports alphabetically
* Introduce routines for manipulating with rules
* :arrow_up: Automatic update of dependencies by Kebechet
* Fix only_if_package_seen logic handling
* Provide force_sync option to solver syncing logic (#2310)
* :arrow_up: Automatic update of dependencies by Kebechet (#2312)
* :whale: update the prow jobs resource requests (#2311)
* :arrow_up: Automatic update of dependencies by Kebechet (#2309)

## Release 0.44.0 (2021-06-03T10:57:21)
### Features
* Create a query for listing rules assigned for a specific package
* :arrow_up: Automatic update of dependencies by Kebechet
* Adjust CVE model to consume vulnerabilities from pypa/advisory-db
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.44.1 (2021-06-03T20:05:50)
### Features
* Cache solver rules retrieval

## Release 0.45.0 (2021-06-07T07:35:06)
### Improvements
* Implement adapter for accessing Argo Workflow logs

## Release 0.45.1 (2021-06-09T11:12:48)
### Features
* missing model import for ExternalPythonSoftwareStack
### Bug Fixes
* Fix unknown index_url in entity when a rule is assigned

## Release 0.46.0 (2021-06-15T08:39:54)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Add method for CVE count
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.47.0 (2021-06-17T15:59:54)
### Features
* Introduce query for retrieving RPM packages for a container image analysis
* add priority/critical-urgent label to all bot related issue templates
* Adjust migrations
* Fail as soon as possible
* Add enum for platform and create migration
* :arrow_up: Automatic update of dependencies by Kebechet
* Filter before session
* make sure os_name is synced correctly in the database
* this is redundant
* :arrow_up: updated labels of issue templates
* :arrow_up: update CI/CD configuration
### Improvements
* adjust method
* make pre-commit happy
* Adjust query and sync logic
* adjust all methods
* :arrow_up: some standard updates or reformatting

## Release 0.48.0 (2021-06-18T08:00:25)
### Features
* Introduce query for obtaining last container image analysis
* Cache query for retrieving RPM versions from the database
* :arrow_up: Automatic update of dependencies by Kebechet
* Cache S2I image symbols query

## Release 0.49.0 (2021-06-21T10:39:47)
### Features
* Introduce query for index bloat data

## Release 0.50.0 (2021-06-29T17:57:39)
### Features
* :cloud: Deprecated the platform column form the dependsOn table
* :arrow_up: Automatic update of dependencies by Kebechet
* add query for filtering git app installations by software environments used
* :medal_sports: set badges for easy access to content (#2372)
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.51.0 (2021-07-01T16:10:08)
### Improvements
* Adjust Python package syncing logic and query for Python packages present

## Release 0.52.0 (2021-07-08T17:17:10)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Adjust return type
* Adjust/Add kebechet managers queries
* Use common enums
* Remove qeb-hwt integration

## Release 0.52.1 (2021-07-12T08:28:15)
### Features
* Adjust query and enums
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.53.0 (2021-07-14T10:47:08)
### Features
* Adjust return value type
* :arrow_up: Automatic update of dependencies by Kebechet
### Improvements
* Extend Python package index with only_packages_seen attribute
* Fix index assignment in solver rule creation

## Release 0.54.0 (2021-07-27T05:47:19)
### Features
* Introduce query for obtaining trove classfiers
