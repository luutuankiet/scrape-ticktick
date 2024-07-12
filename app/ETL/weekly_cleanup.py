#%%

import os,sys; sys.path.append(os.path.dirname(__file__))
from datetime import datetime,timezone

from loader import *
from loader import _delete_tasks

from dagster import op,job,Definitions


from helper.source_env import makefile_path,makefile_dir
import subprocess
#%%



@op
def cleanup():
    TickTickClient._login = new_login
    auth_client = OAuth2(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        cache_path=cache_path
                        )
    client = TickTickClient(username, password, auth_client)
    today = datetime.now(timezone.utc)
    cutoff_date = today - timedelta(days=7)
    # cutoff_date = datetime(2022, 7, 24, tzinfo=timezone.utc)
    start_date = datetime(2024, 7, 1,tzinfo=timezone.utc)
    _delete_tasks(end=cutoff_date,client=client,full_load=False,start=start_date)

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
    



#%%
@job
def weekly_cleanup():
    loader_rerun(cleanup())





# TODO: Call the function to execute the request. last time ended at client.http_delete(url="https://api.ticktick.com/api/v2/user/sessions/others")
# but very dangerous there ran into a bug it constantly logs me out.
# logout_sessions()







defs =  Definitions(jobs=[weekly_cleanup])

#%%





