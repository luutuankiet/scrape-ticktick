# installation

on the very first run, the loader service must be set up once and run indefinitely
`make deploy-from-scratch`


on subsequent run, provided the `loader` session is running, only need to run 
`make deploy`


# prequisite

MUST already have the seeding csv "list_goal_mapping" in `dbt_project/seeds/list_goal_mapping.csv` because this is a seed, and dbt asumes this gets created elsewhere


