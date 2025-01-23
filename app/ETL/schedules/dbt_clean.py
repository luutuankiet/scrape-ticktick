from dagster import ScheduleDefinition
from jobs.dbt_clean import job_dbt_clean

schedule_dbt_clean = ScheduleDefinition(
    name="dbt_clean_weekly",
    job=job_dbt_clean,
    cron_schedule="0 0 * * 6",execution_timezone="Asia/Bangkok"
)
