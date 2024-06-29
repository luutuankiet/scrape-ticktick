# prequisite

download `service_account.json` put it to /workspaces/scrape-ticktick/app/env

MUST already have the seeding csv "list_goal_mapping" in `dbt_project/seeds/list_goal_mapping.csv` because this is a seed, and dbt asumes this gets created elsewhere

use this command to scaffold the seeds (sourced from google sheet) `make init_seed`, THEN continue with `make deploy-from-scratch` below


# development
clone new repo & install requirements
`make init_dev`

# installation

on subsequent run, provided the `loader` session is running, only need to run 
`make deploy`

# fixes when changing to another adpater (duckdb to postgres)
`pip uninstall -y dbt-adapters`
 `pip install --upgrade dbt-adapters dbt-core dbt-common`

## step for prod deploy with postgres
run EL to load raw and create the schema
run seeds
run dbt models


# migration to postgres db
- the raw files must have new names : 
    - tasks_raw.json
    - lists_raw.json
    - folders_raw.json


# to cleanup completed tasks for performance :
- best to use interactive mode, there's a func _delete_task() found in `loader.py`

