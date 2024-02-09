#!/bin/bash


apt-get update && apt-get install -y python3-venv

# init then source env vars
. ./env_init.sh
source .env


# create env
python3 -m venv $VIRTUAL_ENV

# add virt env to PATH
export PATH="$VIRTUAL_ENV/bin:$PATH"

# install dbt deps
# pip install -r containers/dbt/requirements.txt
