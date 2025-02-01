from datetime import datetime,timezone
import shutil
from loader import (
cache_path,
client_id,
client_secret,
username,
password,
redirect_uri,
)
from datetime import datetime, timedelta,timezone

from loader import _delete_tasks
from loader import new_login as t_new_login

from ticktick.oauth2 import OAuth2 as t_OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient as t_TickTickClient   # Main Interface


from dagster import op,job,Definitions,in_process_executor,OpExecutionContext


from helper.source_env import makefile_path,makefile_dir
import subprocess

@op
def cleanup(context: OpExecutionContext):
    t_TickTickClient._login = t_new_login
    t_auth_client = t_OAuth2(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        cache_path=cache_path
                        )
    t_client = t_TickTickClient(username, password, t_auth_client)
    today = datetime.now(timezone.utc)
    cutoff_date = today - timedelta(days=5)
    # cutoff_date = datetime(2022, 7, 24, tzinfo=timezone.utc)
    start_date = today - timedelta(days=14)
    _delete_tasks(context, end=cutoff_date,client=t_client,full_load=False,start=start_date)

@op
def loader_rerun(cleanup):
    # Command to execute 'make' with specified target
    make_cmd = 'loader_rerun'
    command = ['make', '-f', makefile_path, make_cmd]
    
    # Run the command using subprocess
    try:
        subprocess.run(command, check=True,cwd=makefile_dir)
        print(f"Make target '{make_cmd}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing make target '{make_cmd}': {e}")
    


@op
def cleanup_logs_and_artifacts(loader_rerun):
    target_dir = os.getenv('DAGSTER_LOCAL_ARTIFACT_STORAGE_DIR')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        os.makedirs(target_dir)  # Recreate the directory to ensure it exists for future runs
        print(f"Cleaned up directory: {target_dir}")
    else:
        print(f"Directory does not exist: {target_dir}")
@job(executor_def=in_process_executor)
def weekly_cleanup():
    cleanup()
    # cleanup_logs_and_artifacts(loader_rerun(cleanup()))
    






# TODO: Call the function to execute the request. last time ended at client.http_delete(url="https://api.ticktick.com/api/v2/user/sessions/others")
# but very dangerous there ran into a bug it constantly logs me out.
# logout_sessions()







defs =  Definitions(jobs=[weekly_cleanup])


if __name__ == "__main__":
    result = weekly_cleanup.execute_in_process()
    if result.success:
        print("Job executed successfully.")
    else:
        print("Job execution failed.")



