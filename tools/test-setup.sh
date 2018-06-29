#!/bin/bash

# This script will set up our test environment.

LANG=en_US.utf8 
LC_ALL=en_US.utf8

scl enable rh-python36 -- pipenv install --three --dev

#end.