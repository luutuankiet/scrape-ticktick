#%%
import os, sys; sys.path.append(os.path.dirname(__file__)); sys.path.append('..')
import pandas as pd 
import subprocess
from source_env import dbt_project_dir
import io
import tempfile

#%%

# wrapper func for grabbing dbt mf
def invoke_mf(query):
    """
    wrapper func for grabbing dbt mf
    """
    proc=subprocess.run("echo ",shell=True,input="$DBT_PROJECT_DIR")
    output, code = proc.stdout,proc.returncode
    print(output,code)
    return output, code

def run_mf_query(metrics, group_by, end_time=None, start_time=None, where=None, limit=None, order_by=None, compile=False, explain=False, show_dataflow_plan=False, display_plans=False, decimals=None, show_sql_descriptions=False, workdir=dbt_project_dir):
    command = ["mf", "query"]

    # Convert each argument to a raw string if provided
    command.extend(["--metrics", fr"{metrics}"])
    command.extend(["--group-by", fr"{group_by}"])

    if end_time:
        command.extend(["--end-time", fr"{end_time}"])
    if start_time:
        command.extend(["--start-time", fr"{start_time}"])
    if where:
        command.extend(["--where", fr"{where}"])
    if limit:
        command.extend(["--limit", fr"{limit}"])
    if order_by:
        command.extend(["--order-by", fr"{order_by}"])
    # if csv:
    #     command.extend(["--csv", fr"{csv}"])
    if compile:
        command.append("--compile")
    if explain:
        command.append("--explain")
    if show_dataflow_plan:
        command.append("--show-dataflow-plan")
    if display_plans:
        command.append("--display-plans")
    if decimals is not None:
        command.extend(["--decimals", str(decimals)])
    if show_sql_descriptions:
        command.append("--show-sql-descriptions")

    # Execute the command
    try:
        with tempfile.NamedTemporaryFile(mode='r+',suffix='.csv',delete=True) as query_file:
            query_path = query_file.name
            command.extend(["--csv", query_path])

        
        
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=False, cwd=workdir)
        
        # capture output in memory csv
        with open(query_path,'r') as file:
            csv_content = file.read()
        csv_output = io.StringIO(csv_content)
        df = pd.read_csv(csv_output)
        os.remove(query_path)
        
        # print("Command Output:")
        # print(result.stdout)
        if result.stderr:
            print("Command Errors:")
            print(result.stderr)
        return df
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error Output: {e.stderr}")

# Example usage with raw strings and working directory
run_mf_query(
    metrics="task_count_metric",
    group_by="todo_id__folder_dim,todo_id__list_dim,todo_id__completed_date__year"
    
)

# mf query --metrics task_count_metric --group-by todo_id__completed_date__year
# %%
