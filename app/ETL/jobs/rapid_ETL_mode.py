from dagster import Definitions,op,job,in_process_executor,mem_io_manager, OpExecutionContext
import os,time
import subprocess
import helper.source_env
import logging
import shutil

exec_time_minutes = int(os.environ.get('TMP_EXEC_TIME_MINUTES',30))

# job to auto toggle rapid etl sched after specified time
def toggle_rapid_schedule(sequence, context: OpExecutionContext):
    code_location = os.getenv('DAGSTER_CODE_LOCATION_NAME')
    cmd_dagster_1 = f"dagster schedule start --location {code_location} rapid_ETL_schedule && dagster schedule stop --location {code_location} ETL_schedule"
    cmd_dagster_2 = f"dagster schedule stop --location {code_location} rapid_ETL_schedule && dagster schedule start --location {code_location} ETL_schedule"
    cmd = f"{cmd_dagster_1}" if sequence == 1 else f"{cmd_dagster_2}"
    # cmd = f"{cmd_venv} && {cmd_dagster_1}" if sequence == 1 else f"{cmd_venv} && {cmd_dagster_2}"

    context.log.info(f"""
                        running commands: {cmd}
                     """
                     )
    try:
        result = subprocess.run(
            ["/bin/bash", "-c", cmd],
            check=True,
            cwd=os.environ.get("DAGSTER_HOME", "opt/dagster/dagster_home"),
            env=os.environ,
            capture_output=True,
            text=True  # Ensure the output is captured as a string
        )
        
        # Log the stderr output
        if result.stdout:
            context.log.info(f"stdout: {result.stdout}")
        if result.stderr:
            context.log.info(f"stderr: {result.stderr}")

    except Exception as e:
        raise Exception(f"Failed to toggle ETL rapid schedule: {e}")
@op
def schedule_toggle(context: OpExecutionContext):
    context.log.info(f"rapid_ETL_schedule is ON. sleeping for {exec_time_minutes} minutes.")
    toggle_rapid_schedule(1, context)
    time.sleep(exec_time_minutes*60)
    toggle_rapid_schedule(2, context)




@job(executor_def=in_process_executor)
def rapid_ETL_mode():
    schedule_toggle()

defs = Definitions(jobs=[rapid_ETL_mode],
    resources={
        "io_manager": mem_io_manager
    })
