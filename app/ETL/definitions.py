import os

from dagster import Definitions
# from dagster_dbt import DbtCliResource

# from .dbt_assets import ticktick_dbt_assets
# from .EL import *
# from .constants import dbt_project_dir

from .EL import get_all_tasks,dump_to_file,get_lists,get_folders,dump_to_motherduck

defs = Definitions(
    assets=[
            get_all_tasks,
            get_lists,
            get_folders,
            dump_to_file,
            dump_to_motherduck
            ],
    # resources={
    #     "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    # },
)

