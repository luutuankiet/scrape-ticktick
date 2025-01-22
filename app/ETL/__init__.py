import os,sys; sys.path.append(os.path.dirname(__file__))
from dagster import Definitions,ScheduleDefinition,define_asset_job,load_assets_from_modules,in_process_executor,mem_io_manager
from dagster_dbt import DbtCliResource
from sqlalchemy import true

from constants import DBT_DIR,dbt
import EL,dbt_assets
from lvl3_helper import load_new_lvl3_data,load_mapping_helper
from weekly_cleanup import weekly_cleanup
from job_rapid_ETL_mode import rapid_ETL_mode
from job_deploy_LD import job_deploy_LD
from job_add_stale_tag import job_add_stale_tags


all_assets = load_assets_from_modules([EL,dbt_assets])
ETL_job = define_asset_job(
    "ETL_job",selection=[
                dbt_assets.ticktick_dbt_assets,
                EL.init_extract,
                EL.raw_data
            ],
    executor_def=in_process_executor,
    config={"ops": {"ticktick_dbt_assets": {"config": {"cli_args": ["run"]}}}}
    )

ETL_full_job = define_asset_job(
    name="ETL_full_job",
    selection=[dbt_assets.ticktick_dbt_assets,
               EL.init_extract,
               EL.raw_data
               ],
    config={"ops": {"ticktick_dbt_assets": {"config": {"cli_args": ["build"]}}}},
    executor_def=in_process_executor
)

ETL_full_schedule = ScheduleDefinition(
    name="ETL_full_schedule",
    job=ETL_full_job,
    cron_schedule="0 21 * * 6",execution_timezone="Asia/Bangkok"
)

ETL_schedule = ScheduleDefinition(
    name="ETL_schedule",
    job=ETL_job,
    cron_schedule="0,30 4-22 * * *",execution_timezone="Asia/Bangkok"
)
rapid_ETL_schedule = ScheduleDefinition(
    name="rapid_ETL_schedule",
    job=ETL_job,
    cron_schedule="* * * * *",execution_timezone="Asia/Bangkok"
)


helper_schedule = ScheduleDefinition(
    job=load_mapping_helper,
    cron_schedule="0,30 4-22 * * *",execution_timezone="Asia/Bangkok"
)

cleanup_schedule = ScheduleDefinition(
    job=weekly_cleanup,
    cron_schedule="0 0 * * 5",execution_timezone="Asia/Bangkok"
)

deploy_schedule = ScheduleDefinition(
    job=job_deploy_LD,
    cron_schedule="0 4 * * *",execution_timezone="Asia/Bangkok"
)


defs = Definitions(
    assets=all_assets,
    jobs=[
        load_new_lvl3_data,
        weekly_cleanup,
        rapid_ETL_mode,
        job_deploy_LD,
        job_add_stale_tags,
        ETL_job,
        ETL_full_job
          ],
    schedules=[ETL_schedule,
               ETL_full_schedule,
               rapid_ETL_schedule,
               helper_schedule,
               cleanup_schedule,
               deploy_schedule
               ],
    resources={
        "dbt": dbt,
        "io_manager": mem_io_manager,
    },
)

