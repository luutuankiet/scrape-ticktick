# need this line to make the imports work
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from dagster import (
    Definitions,
    ScheduleDefinition,
    load_assets_from_modules,
    in_process_executor,
    InMemoryIOManager,
)
from constants import dbt
import assets.EL as EL
import assets.dbt_assets as dbt_assets

from jobs.dbt_jobs import ETL_job, ETL_full_job
from jobs.lvl3_helper import load_new_lvl3_data, load_mapping_helper
from jobs.weekly_cleanup import weekly_cleanup
from jobs.rapid_ETL_mode import rapid_ETL_mode
from jobs.deploy_LD import job_deploy_LD
from jobs.add_stale_tag import job_add_stale_tags
from jobs.dbt_clean import job_dbt_clean


all_assets = load_assets_from_modules([EL, dbt_assets])


ETL_full_schedule = ScheduleDefinition(
    name="ETL_full_schedule",
    job=ETL_full_job,
    cron_schedule="0 21 * * 6",
    execution_timezone="Asia/Bangkok",
)

ETL_schedule = ScheduleDefinition(
    name="ETL_schedule",
    job=ETL_job,
    cron_schedule="0,30 4-22 * * *",
    execution_timezone="Asia/Bangkok",
)

rapid_ETL_schedule = ScheduleDefinition(
    name="rapid_ETL_schedule",
    job=ETL_job,
    cron_schedule="* * * * *",
    execution_timezone="Asia/Bangkok",
)


helper_schedule = ScheduleDefinition(
    job=load_mapping_helper,
    cron_schedule="0,30 4-22 * * *",
    execution_timezone="Asia/Bangkok",
)

cleanup_schedule = ScheduleDefinition(
    job=weekly_cleanup, cron_schedule="0 0 * * 5", 
    execution_timezone="Asia/Bangkok"
)

deploy_schedule = ScheduleDefinition(
    job=job_deploy_LD, cron_schedule="0 4 * * *", 
    execution_timezone="Asia/Bangkok"
)

schedule_dbt_clean = ScheduleDefinition(
    name="dbt_clean_weekly",
    job=job_dbt_clean,
    cron_schedule="0 0 * * 6",
    execution_timezone="Asia/Bangkok",
)

all_jobs = [
    load_new_lvl3_data,
    weekly_cleanup,
    rapid_ETL_mode,
    job_deploy_LD,
    job_add_stale_tags,
    ETL_job,
    ETL_full_job,
    job_dbt_clean,
]

all_schedules = [
    ETL_schedule,
    ETL_full_schedule,
    rapid_ETL_schedule,
    helper_schedule,
    cleanup_schedule,
    deploy_schedule,
    schedule_dbt_clean,
]

all_resources = {
    "dbt": dbt,
    "io_manager": InMemoryIOManager(),
}


defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
    resources=all_resources,
    executor=in_process_executor,
)
