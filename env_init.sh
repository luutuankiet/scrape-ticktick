# parse dir 
ENV_WORK_DIR=$(pwd)

cat <<EOF > .env
VIRTUAL_ENV="$ENV_WORK_DIR/.venv"
DBT_PROJECT_DIR="$ENV_WORK_DIR/dbt_project"
DBT_PROFILES_DIR="$ENV_WORK_DIR/dbt_project"
DW_PATH="$ENV_WORK_DIR/database/memory.duckdb"
DAGSTER_HOME="$ENV_WORK_DIR"
PYTHONPATH="$ENV_WORK_DIR/app"
ST_LOGS_PATH="$ENV_WORK_DIR/streamlit_logs/logs.txt"
DW_USER="ken"
DW_PASSWORD="Boyluu96@"
DW_DBNAME="gtd_dash"
EOF

# source env
# . ./.env