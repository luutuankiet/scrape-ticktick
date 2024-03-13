#%%
import sys; sys.path.append('..')
import os
from dagster import OpExecutionContext, OpDefinition, op
from helper.source_env import dbt_project_dir,service_account_path
import duckdb
import gspread

#%%


analyses_path = os.path.join(dbt_project_dir,'target/compiled/todo_analytics/analyses')
helper_query_path = os.path.join(analyses_path,'lvl3_helper_list_extract.sql')
motherduck_token = os.environ.get("motherduck_token")
with open(helper_query_path,'r') as f:
    helper_query = f.read()
con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()
client = gspread.service_account(service_account_path)


def generate_helper_data():
    helper_df = cur.sql(helper_query).df()
    workbook = client.open_by_url("https://docs.google.com/spreadsheets/d/1My7VU0GrAlYTa46Hj1ciOBXivcF7QKSYeRVXXbyV74o/edit#gid=0")
    helper_sheet = workbook.get_worksheet(2)
    
    # clears the sheet
    helper_sheet.clear()


    # writes the lists 
    helper_sheet.update("A1",values =[helper_df.columns.tolist()] + helper_df.values.tolist())

    # writes the latest goals
    goals_query = "select goal_id,goal_name from init_duckdb__lvl3 order by 1"
    goals_df = cur.sql(goals_query).df()
    helper_sheet.update("D1",values =[goals_df.columns.tolist()] + goals_df.values.tolist())


# %%

seed_query = "select * from list_goal_mapping"
seed_df = cur.sql(seed_query).df()

# %%
