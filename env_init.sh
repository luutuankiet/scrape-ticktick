# parse dir 
ENV_WORK_DIR=$(pwd)

cat <<EOF > .env
export VIRTUAL_ENV="$ENV_WORK_DIR/.venv"
export DBT_PROJECT_DIR="$ENV_WORK_DIR/dbt_project"
export DBT_PROFILES_DIR="$ENV_WORK_DIR/dbt_project"
export DW_PATH="$ENV_WORK_DIR/database"
EOF