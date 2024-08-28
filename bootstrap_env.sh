#!/bin/bash

ENV_WORK_DIR=$(pwd)

# Function to initialize .env file
init_env() {
# Add more environment variables here if needed
    cat > ".env.bootstrap" <<EOENV
VIRTUAL_ENV="$ENV_WORK_DIR/.venv"
PYTHONPATH="$ENV_WORK_DIR/app"
DBT_PROJECT_DIR="$ENV_WORK_DIR/dbt_project"
DBT_PROFILES_DIR="$ENV_WORK_DIR/dbt_project"

DAGSTER_HOME="$ENV_WORK_DIR"
DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1
DAGSTER_LOCAL_ARTIFACT_STORAGE_DIR="$ENV_WORK_DIR/dagster_artifacts"

MAKEFILE_PATH="$ENV_WORK_DIR/Makefile"

EOENV
}

# Function to source .env file
source_env() {
    set -a  # Automatically export all variables
    . ./.env.bootstrap
    if [ ! -f .env ]; then
        touch .env
    fi
    . ./.env
    set +a  # Stop automatically exporting variables
}

# Invoke init_env and source_env functions
init_env
source_env

