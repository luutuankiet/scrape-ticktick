#!/bin/bash

ENV_WORK_DIR=$(pwd)

# Function to initialize .env file
init_env() {
# Add more environment variables here if needed
    cat > ".env" <<EOENV
VIRTUAL_ENV="$ENV_WORK_DIR/.venv"
DBT_PROJECT_DIR="$ENV_WORK_DIR/dbt_project"
DBT_PROFILES_DIR="$ENV_WORK_DIR/dbt_project"
DW_PATH="$ENV_WORK_DIR/database/memory.duckdb"
DAGSTER_HOME="$ENV_WORK_DIR"
PYTHONPATH="$ENV_WORK_DIR/app"
DW_USER="ken"
DW_PASSWORD="Boyluu96"
DW_DBNAME="gtd_dash"
DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1

EOENV
}

# Function to source .env file
source_env() {
    set -a  # Automatically export all variables
    source .env
    set +a  # Stop automatically exporting variables
}

# Invoke init_env and source_env functions
init_env
source_env

