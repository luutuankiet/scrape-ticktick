#!/bin/bash


apt-get update && apt-get install -y python3-venv

# init then source env vars
chmod +x ./env_init.sh
chmod +x ./source_env.sh

. ./env_init.sh
source source_env.sh


# create env
python3 -m venv $VIRTUAL_ENV

# add virt env to PATH
export PATH="$VIRTUAL_ENV/bin:$PATH"

# install reqs
pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade requests urllib3 chardet charset_normalizer # address a bug url lib version incompatibility

# run dbt 
dbt deps
dbt build