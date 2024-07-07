#%%
import os
import sys; sys.path.append('..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from helper.source_env import dbt_project_dir,service_account_path,dw_path
import gspread
import csv
from dagster import op,Definitions,job
from sqlalchemy import create_engine,text
from EL import db_url
import pandas as pd

#%%




analyses_path = os.path.join(dbt_project_dir,'target/compiled/todo_analytics/analyses')
helper_query_path = os.path.join(analyses_path,'lvl3_helper_list_extract.sql')
seed_path = os.path.join(dbt_project_dir,'seeds/list_goal_mapping.csv')
with open(helper_query_path,'r') as f:
    helper_query = f.read()

conn = create_engine(db_url)
# con = duckdb.connect(read_only=False)
# con.sql(f"IMPORT DATABASE '{os.path.dirname(dw_path)}/src';")

client = gspread.service_account(service_account_path)
workbook = client.open_by_url("https://docs.google.com/spreadsheets/d/1My7VU0GrAlYTa46Hj1ciOBXivcF7QKSYeRVXXbyV74o/edit#gid=0")
helper_sheet = workbook.get_worksheet(1)
mapping_sheet = workbook.get_worksheet(0)

@op
def mapping_helper():
    """
    insert into the mapping_herlper sheet the goals selected from db
    """
    with conn.connect() as con:
        helper_df = pd.read_sql(helper_query,con=con)
    
        # clears the sheet
        helper_sheet.clear()


        # writes the lists 
        helper_sheet.update("A1",values =[helper_df.columns.tolist()] + helper_df.values.tolist())

        # writes the latest goals
        goals_query = "select goal_id,goal_name from init_duckdb__lvl3 order by 1"
        goals_df = pd.read_sql(goals_query,con=con)
        helper_sheet.update("D1",values =[goals_df.columns.tolist()] + goals_df.values.tolist())


# @op
# def mapping_helper():
#     """
#     insert into the mapping_herlper sheet the goals selected from db
#     """
#     helper_df = con.sql(helper_query).df()
    
#     # clears the sheet
#     helper_sheet.clear()


#     # writes the lists 
#     helper_sheet.update("A1",values =[helper_df.columns.tolist()] + helper_df.values.tolist())

#     # writes the latest goals
#     goals_query = "select goal_id,goal_name from init_duckdb__lvl3 order by 1"
#     goals_df = con.sql(goals_query).df()
#     helper_sheet.update("D1",values =[goals_df.columns.tolist()] + goals_df.values.tolist())
#     con.close()
@op
def load_mapping_to_stg():
    stg_data = helper_sheet.get_values('A:C')
    mapping_sheet.clear()
    mapping_sheet.update("A1",values =stg_data)


@op
def dump_mapping_to_csv(results=None):
    with open(seed_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(mapping_sheet.get_values())




@job
def load_new_lvl3_data():
    dump_mapping_to_csv(load_mapping_to_stg())

@job
def load_mapping_helper():
    mapping_helper()

defs =  Definitions(jobs=[load_new_lvl3_data,load_mapping_helper])