import os
from dagster import Definitions, AssetSelection,ScheduleDefinition,define_asset_job,load_assets_from_modules
from dagster_dbt import DbtCliResource
# from .dbt_assets import ticktick_dbt_assets

from .constants import DBT_PROJECT_DIR
# from .EL import get_all_tasks,dump_to_file,get_lists,get_folders,dump_to_motherduck
from. import EL,dbt_assets

all_assets = load_assets_from_modules([EL,dbt_assets])
# ETL_job = define_asset_job("ETL_job",selection=AssetSelection.all())
ETL_job = define_asset_job("ETL_job",selection=all_assets)
ETL_schedule = ScheduleDefinition(
    job=ETL_job,
    cron_schedule="0 12,14,16,20,22 * * *",execution_timezone="Asia/Bangkok"
)

defs = Definitions(
    assets=all_assets,
    schedules=[ETL_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
    },
)

