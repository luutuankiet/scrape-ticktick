#!/bin/bash

##### install npm
# installs nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# download and install Node.js
nvm install 20

# verifies the right Node.js version is in the environment
node -v # should print `v20.13.1`

# verifies the right NPM version is in the environment
npm -v # should print `10.5.2`



#### sets up python

apt-get update && apt-get install -y python3-venv

# init then source env vars
chmod +x ./env_init.sh
chmod +x ./source_env.sh

. ./env_init.sh
source source_env.sh


# create env
python3 -m venv $VIRTUAL_ENV

# add virt env to PATH which allows the next part of script to install packages directly to venv
export PATH="$VIRTUAL_ENV/bin:$PATH"

# install reqs
pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade requests urllib3 chardet charset_normalizer # address a bug url lib version incompatibility

# run dbt 
dbt deps
dbt build