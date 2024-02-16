import os
from dagster import Definitions
from dagster_dbt import DbtCliResource
from .dbt_assets import ticktick_dbt_assets
from .constants import DBT_PROJECT_DIR
from .EL import get_all_tasks,dump_to_file,get_lists,get_folders,dump_to_motherduck

defs = Definitions(
    assets=[
            get_all_tasks,
            get_lists,
            get_folders,
            dump_to_file,
            dump_to_motherduck,
            ticktick_dbt_assets
            ],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
    },
)

