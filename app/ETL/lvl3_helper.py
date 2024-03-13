#%%
import sys; sys.path.append('/home/ken/dev-main/scrape-ticktick-1/app')
import os
from dagster import OpExecutionContext, OpDefinition, op
from helper.source_env import dbt_project_dir,service_account_path
import duckdb
import gspread

#%%


analyses_path = os.path.join(dbt_project_dir,'target/compiled/todo_analytics/analyses')
helper_query_path = os.path.join(analyses_path,'lvl3_helper_list_extract.sql')
motherduck_token = os.environ.get("motherduck_token")

helper_query = open(helper_query_path,'r').read()

con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()

helper_df = cur.sql(helper_query).df()

#%%
client = gspread.service_account(service_account_path)
workbook = client.open_by_url("https://docs.google.com/spreadsheets/d/1My7VU0GrAlYTa46Hj1ciOBXivcF7QKSYeRVXXbyV74o/edit#gid=0")
helper_sheet = workbook.get_worksheet(2)
helper_sheet.update([helper_df.columns.tolist()] + helper_df.values.tolist())







# %%
