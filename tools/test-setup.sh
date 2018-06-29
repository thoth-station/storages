#!/bin/bash

# This script will set up our test environment.

scl enable rh-python36 -- LANG=en_US.utf8  LC_ALL=en_US.utf8 pipenv install --three --dev

#end.