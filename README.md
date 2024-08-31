[![CD](https://github.com/luutuankiet/scrape-ticktick/actions/workflows/gh_deploy.yml/badge.svg)](https://github.com/luutuankiet/scrape-ticktick/actions/workflows/gh_deploy.yml)

# prequisite

download `service_account.json` put it to /workspaces/scrape-ticktick/app/env

MUST already have the seeding csv "list_goal_mapping" in `dbt_project/seeds/list_goal_mapping.csv` because this is a seed, and dbt asumes this gets created elsewhere

use this command to scaffold the seeds (sourced from google sheet) `make init_seed`, THEN continue with `make deploy-from-scratch` below

for vs code intergrated terminal : add this line to bashrc/zshrc/powershell or whichever your default vs code default terminal uses
. /workspaces/scrape-ticktick/bootstrap_env.sh



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
- remember to update the gsheets the column name to the new models standard name



# to cleanup completed tasks for performance :
- best to use interactive mode, there's a func _delete_task() found in `loader.py`


# utils
- install webhook to allow run dagstger from a url : `sudo apt-get install webhook`

# development
- after each model update, should do a full dagster reload definitions for it to parse new models
