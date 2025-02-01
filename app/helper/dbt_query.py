#%%
import pandas as pd 
import subprocess
from source_env import dbt_project_dir
import io
import tempfile

#%%

# wrapper func for grabbing dbt mf

def run_mf_query(debug=False,metrics=None, group_by=None, end_time=None, start_time=None, where=None, limit=None, order_by=None, compile=False, explain=False, show_dataflow_plan=False, display_plans=False, decimals=None, show_sql_descriptions=False, workdir=dbt_project_dir):
    command = ["mf", "query"]
    """
    wrapper func to execute mf query for metrics. only different arg is csv where we write to a pseudo in mem file instead.
    if debug=True, preforms mf and output to stdout. otherwise returns a df.
    Options:

  --metrics SEQUENCE       Metrics to query for: syntax is --metrics bookings
                           or for multiple metrics --metrics bookings, messages.

  --group-by SEQUENCE      Dimensions and/or entities to group by: syntax is
                           --group-by ds or for multiple group bys --group-by
                           ds, org.

  --end-time TEXT          Optional iso8601 timestamp to constraint the end
                           time of the data (inclusive).
                           *Not available in dbt Cloud yet 

  --start-time TEXT        Optional iso8601 timestamp to constraint the start
                           time of the data (inclusive)
                           *Not available in dbt Cloud yet

  --where TEXT             SQL-like where statement provided as a string. For
                           example: --where "revenue > 100". To add a dimension filter to 
                           a where filter, you have to indicate that the filter item is part of your model. 
                           Refer to the FAQ for more info on how to do this using a template wrapper.

  --limit TEXT             Limit the number of rows out using an int or leave
                           blank for no limit. For example: --limit 100

  --order-by SEQUENCE         Metrics or group bys to order by ("-" prefix for
                           DESC). For example: --order-by -ds or --order-by
                           ds,-revenue

 --compile (dbt Cloud)    In the query output, show the query that was
 --explain (dbt Core)     executed against the data warehouse         
                           

  --show-dataflow-plan     Display dataflow plan in explain output

  --display-plans          Display plans (such as metric dataflow) in the browser

  --decimals INTEGER       Choose the number of decimal places to round for
                           the numerical values

  --show-sql-descriptions  Shows inline descriptions of nodes in displayed SQL

  --help                   Show this message and exit.

  # Example usage with raw strings and working directory
run_mf_query(
    metrics="task_count_metric",
    group_by="todo_id__folder_dim,todo_id__list_dim,todo_id__completed_date__year"
    
)

    """

    # Convert each argument to a raw string if provided
    command.extend(["--metrics", fr"{metrics}"])
    command.extend(["--group-by", fr"{group_by}"]) if group_by else None

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
        if debug==False:
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
            return df

        if debug==True:
            result = subprocess.run(command, capture_output=True, text=True, check=True, shell=False, cwd=workdir)
            print("Command Output:")
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error Output: {e.stderr}")


# mf query --metrics task_count_metric --group-by todo_id__completed_date__year
# %%
