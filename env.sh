#!/bin/bash

ENV_WORK_DIR=$(pwd)

# Function to initialize .env file
init_env() {
# Add more environment variables here if needed
    cat > ".env" <<EOENV
VIRTUAL_ENV="$ENV_WORK_DIR/.venv"
PYTHONPATH="$ENV_WORK_DIR/app"
DBT_PROJECT_DIR="$ENV_WORK_DIR/dbt_project"
DBT_PROFILES_DIR="$ENV_WORK_DIR/dbt_project"

DW_USER="ken"
DW_PASSWORD="Boyluu96"
DW_DBNAME="gtd_dash"
DW_HOST="boyluu0819.ddns.net"
DW_PORT="5433"

DAGSTER_HOME="$ENV_WORK_DIR"
DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1
DAGSTER_LOCAL_ARTIFACT_STORAGE_DIR="$ENV_WORK_DIR/dagster_artifacts"
DAGSTER_PG_USERNAME="ken"
DAGSTER_PG_PASSWORD="Boyluu96"
DAGSTER_PG_HOST="boyluu0819.ddns.net"
DAGSTER_PG_DB="gtd_dash"

EOENV
}

# Function to source .env file
source_env() {
    set -a  # Automatically export all variables
    . ./.env
    set +a  # Stop automatically exporting variables
}

# Invoke init_env and source_env functions
init_env
source_env

