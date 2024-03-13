from json import load
import os
from dagster import Definitions,ScheduleDefinition,define_asset_job,load_assets_from_modules
from dagster_dbt import DbtCliResource

from .constants import DBT_PROJECT_DIR
from . import EL,dbt_assets
from .lvl3_helper import load_new_lvl3_data,load_mapping_helper

all_assets = load_assets_from_modules([EL,dbt_assets])
ETL_job = define_asset_job("ETL_job",selection=all_assets)
ETL_schedule = ScheduleDefinition(
    job=ETL_job,
    cron_schedule="*/30 * * * *",execution_timezone="Asia/Bangkok"
)


helper_schedule = ScheduleDefinition(
    job=load_mapping_helper,
    cron_schedule="*/30 * * * *",execution_timezone="Asia/Bangkok"
)


defs = Definitions(
    assets=all_assets,
    jobs=[load_new_lvl3_data],
    schedules=[ETL_schedule,helper_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
    },
)

