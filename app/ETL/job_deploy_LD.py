#%%
from importlib import resources
from dagster import job, mem_io_manager,op, Definitions, mem_io_manager,in_process_executor
import os, subprocess
import helper.source_env



@op
def deploy_LD():
    cmd_venv = "source .venv/bin/activate"
    LD_cmd = "lightdash deploy"
    cmd = f"{cmd_venv} && {LD_cmd}"

    result = subprocess.run(
        ["/bin/bash","-c",cmd],
        check=True,
        cwd=os.environ.get("DAGSTER_HOME"),
        env=os.environ
    )
    if result.returncode != 0:
        raise Exception("Failed to toggle ETL rapid schedule")
    

@job(executor_def=in_process_executor)
def job_deploy_LD():
    deploy_LD()

defs = Definitions(jobs=[job_deploy_LD],
                   resources={
                       "io_manager": mem_io_manager
                   }
)
    
#%%