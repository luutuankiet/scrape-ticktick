
# prequisite

MUST already have the seeding csv "list_goal_mapping" in `dbt_project/seeds/list_goal_mapping.csv` because this is a seed, and dbt asumes this gets created elsewhere

use this command to scaffold the seeds (sourced from google sheet) `make init_seed`, THEN continue with `make deploy-from-scratch` below


# installation

on the very first run, the loader service must be set up once and run indefinitely
`make deploy-from-scratch`


on subsequent run, provided the `loader` session is running, only need to run 
`make deploy`

# fixes when changing to another adpater (duckdb to postgres)
`pip uninstall -y dbt-adapters`
 `pip install --upgrade dbt-adapters dbt-core dbt-postgres dbt-common dagster-dbt`


