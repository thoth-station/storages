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
