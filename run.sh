#!/bin/bash

export DAGSTER_HOME=`dirname "$0"|realpath`

poetry run dagster dev \
-m dagsterproject \
-m dagster_example \
"$@"
