#%%
import os,sys; sys.path.append(os.path.dirname(__file__))
from dagster import Definitions,ScheduleDefinition,define_asset_job,load_assets_from_modules,in_process_executor,mem_io_manager
from dagster_dbt import DbtCliResource
from sqlalchemy import true

from constants import DBT_DIR
import EL,dbt_assets
from lvl3_helper import load_new_lvl3_data,load_mapping_helper
from weekly_cleanup import weekly_cleanup
from job_rapid_ETL_mode import rapid_ETL_mode
from job_deploy_LD import job_deploy_LD


#%%
all_assets = load_assets_from_modules([EL,dbt_assets])
ETL_job = define_asset_job("ETL_job",selection=all_assets,executor_def=in_process_executor)
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
    jobs=[load_new_lvl3_data,weekly_cleanup,rapid_ETL_mode,job_deploy_LD],
    schedules=[ETL_schedule,rapid_ETL_schedule,helper_schedule,cleanup_schedule,deploy_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_DIR),
        "io_manager": mem_io_manager,
    },
)

