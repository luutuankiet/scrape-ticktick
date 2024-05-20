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
motherduck_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uIjoibHV1dHVhbmtpZXQuZnR1Mi5nbWFpbC5jb20iLCJlbWFpbCI6Imx1dXR1YW5raWV0LmZ0dTJAZ21haWwuY29tIiwidXNlcklkIjoiMjRkOTQxYzktMDg2OC00ZThmLWIwNjMtNDFmNjE2MDYyMjMxIiwiaWF0IjoxNzA3MTU2NzY2LCJleHAiOjE3Mzg3MTQzNjZ9.z-FjZKJ8oAewQKJ2X3_4emnJXszt1q_VaB0ZVOsQEUM"
EOF

# source env
# . ./.env