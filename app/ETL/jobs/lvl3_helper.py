#%%
import os
from helper.source_env import dbt_project_dir,service_account_path
import gspread
import csv
from dagster import op,Definitions,job,in_process_executor
from sqlalchemy import create_engine,text
from assets.EL import db_url
import pandas as pd
from constants import dbt
from dagster import Out, Nothing


goals_query = """
select todo_title from
prod.fact_todos where 
todo_list_name = 'lvl3 - 1 - 2 years goals' 
and todo_tags = 'default'
order by todo_sortorder
"""


analyses_path = os.path.join(dbt_project_dir,'target/compiled/todo_analytics/analyses')
helper_query_path = os.path.join(analyses_path,'lvl3_helper_list_extract.sql')
seed_path = os.path.join(dbt_project_dir,'seeds/list_goal_mapping.csv')
with open(helper_query_path,'r') as f:
    helper_query = f.read()


client = gspread.service_account(service_account_path)
workbook = client.open_by_url("https://docs.google.com/spreadsheets/d/1My7VU0GrAlYTa46Hj1ciOBXivcF7QKSYeRVXXbyV74o/edit#gid=0")
helper_sheet = workbook.get_worksheet(1)
mapping_sheet = workbook.get_worksheet(0)

conn = create_engine(db_url)


def load_df_to_sheet(sheet: gspread.worksheet.Worksheet, df: pd.DataFrame, cell :str) -> None:
    """takes the df and writes it to the sheet

    Args:
        sheet (gspread.worksheet.Worksheet): _description_
        df (pd.DataFrame): _description_
        cell (str): _description_
    """
    df_list = [df.columns.tolist()] + df.fillna("").values.tolist()
    sheet.update(cell, df_list)




@op
def mapping_helper():
    """
    grabs the following from db
    - all lists, BOTH mapped and unmapped
    - all goals

    and writes them to the helper sheet

    """

    with conn.connect() as con:
        # clears the sheet
        helper_sheet.clear()

        # writes the lists 
        helper_df = pd.read_sql(helper_query,con=con)
        load_df_to_sheet(helper_sheet,helper_df,"A1")


        # writes the latest goals
        goals_df = pd.read_sql(goals_query,con=con)
        load_df_to_sheet(helper_sheet,goals_df,"D1")



@op
def load_mapping_to_stg():
    stg_data = helper_sheet.get_values('A:C')
    mapping_sheet.clear()
    mapping_sheet.update("A1",stg_data)


@op
def dump_mapping_to_csv(results=None):
    with open(seed_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(mapping_sheet.get_values())


@op(out=Out(Nothing))
def dbt_seeds(results=None):
    """invoke the dbt seed command for list_goal_mapping
    """
    dbt.cli(["seed", "-s", "list_goal_mapping"])


@job(executor_def=in_process_executor)
def load_mapping_helper():
    mapping_helper()


@job(executor_def=in_process_executor)
def load_new_lvl3_data():
    dbt_seeds(dump_mapping_to_csv(load_mapping_to_stg()))

defs =  Definitions(jobs=[load_new_lvl3_data,load_mapping_helper])

