from dagster import Definitions,op,job,in_process_executor,mem_io_manager
import os,time,sys; sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import subprocess
import helper.source_env
import logging
import shutil

exec_time_minutes = int(os.environ.get('TMP_EXEC_TIME_MINUTES',30))

# job to auto toggle rapid etl sched after specified time
def toggle_rapid_schedule(sequence):
    cmd_venv = "source .venv/bin/activate"
    cmd_dagster_1 = "dagster schedule start -m ETL rapid_ETL_schedule && dagster schedule stop -m ETL ETL_schedule"
    cmd_dagster_2 = "dagster schedule stop -m ETL rapid_ETL_schedule && dagster schedule start -m ETL ETL_schedule"
    cmd = f"{cmd_venv} && {cmd_dagster_1}" if sequence == 1 else f"{cmd_venv} && {cmd_dagster_2}"

    result = subprocess.run(
        ["/bin/bash","-c",cmd],
        check=True,
        cwd=os.environ.get("DAGSTER_HOME"),
        env=os.environ
    )
    if result.returncode != 0:
        raise Exception("Failed to toggle ETL rapid schedule")
@op
def schedule_toggle():
    logging.info(f"rapid_ETL_schedule is ON. sleeping for {exec_time_minutes} minutes.")
    toggle_rapid_schedule(1)
    time.sleep(exec_time_minutes*60)
    toggle_rapid_schedule(2)




@job(executor_def=in_process_executor)
def rapid_ETL_mode():
    schedule_toggle()

defs = Definitions(jobs=[rapid_ETL_mode],
    resources={
        "io_manager": mem_io_manager
    })
