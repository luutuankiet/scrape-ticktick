from dagster import Definitions,op,job,in_process_executor
import os,time,sys; sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import subprocess
import helper.source_env

# job to auto toggle rapid etl sched after 30m
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
    toggle_rapid_schedule(1)
    time.sleep(30*60)
    toggle_rapid_schedule(2)



@job
def rapid_ETL_mode():
    schedule_toggle()

defs = Definitions(jobs=[rapid_ETL_mode],executor=in_process_executor)