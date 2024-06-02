#%%
import os
from dagster import AssetMaterialization, Output, asset,AssetExecutionContext,AssetOut, multi_asset, AssetKey, op
from dagster_dbt import get_asset_keys_by_output_name_for_source
import pandas as pd
import sys; sys.path.append('..') # to allow import helper which is 1 dir away
from helper.source_env import raw_path,dw_path,ETL_workdir,db_url,target_schema
import dbt_assets
import time
from sqlalchemy import create_engine
#%%


@asset()
def init_extract():
    flag = os.path.join(ETL_workdir,'force_sync.flag')
    with open(flag, 'w') as f:
        pass
    while True:
        if os.path.exists(flag):
            time.sleep(1)
        else:
            break


@multi_asset(
    outs={
        name: AssetOut(key=asset_key)
        for name, asset_key in get_asset_keys_by_output_name_for_source(
            [dbt_assets.ticktick_dbt_assets], "raw_data"
        ).items()
    },
    compute_kind='python',deps=[init_extract]
)
def dump_postgres(context: AssetExecutionContext):

    
    names = ['source_todo_analytics_raw_data_tasks_raw', 'source_todo_analytics_raw_data_lists_raw', 'source_todo_analytics_raw_data_folders_raw']

    tasks_path = os.path.join(raw_path,'tasks.json')
    tasks_df = pd.read_json(tasks_path,dtype=str)
    lists_path = os.path.join(raw_path,'lists.json')
    lists_df = pd.read_json(lists_path,dtype=str)
    folders_path = os.path.join(raw_path,'folders.json')
    folders_df = pd.read_json(folders_path,dtype=str)
    entity_df = [tasks_df,lists_df,folders_df]

    # Convert all columns to lowercase
    tasks_df.columns = tasks_df.columns.str.lower()
    lists_df.columns = lists_df.columns.str.lower()
    folders_df.columns = folders_df.columns.str.lower()

    engine = create_engine(db_url)
    tasks_df.to_sql('tasks_raw', engine, if_exists='replace', index=False, schema=target_schema)
    lists_df.to_sql('lists_raw', engine, if_exists='replace', index=False,schema=target_schema)
    folders_df.to_sql('folders_raw', engine, if_exists='replace', index=False,schema=target_schema)

    # yield the materialization result
    for name, entity_df in zip(names,entity_df):
        yield Output(entity_df,output_name=name)




# def dump_to_motherduck(context: AssetExecutionContext):

#     names = ['source_todo_analytics_raw_data_tasks_raw', 'source_todo_analytics_raw_data_lists_raw', 'source_todo_analytics_raw_data_folders_raw']

#     tasks_path = os.path.join(raw_path,'tasks.json')
#     tasks_df = pd.read_json(tasks_path,dtype=str)
#     lists_path = os.path.join(raw_path,'lists.json')
#     lists_df = pd.read_json(lists_path,dtype=str)
#     folders_path = os.path.join(raw_path,'folders.json')
#     folders_df = pd.read_json(folders_path,dtype=str)
#     entity_df = [tasks_df,lists_df,folders_df]

#     duckdb.close()
#     con = duckdb.connect(read_only=False)
# # con = duckdb.connect(dw_path,read_only=True)
#     con.sql("""CREATE OR REPLACE TABLE tasks_raw as SELECT * FROM tasks_df;
#             CREATE OR REPLACE TABLE lists_raw as SELECT * FROM lists_df;
#             CREATE OR REPLACE TABLE folders_raw as SELECT * FROM folders_df
#             """)
#     con.sql(f"EXPORT DATABASE '{os.path.dirname(dw_path)}/src' (FORMAT PARQUET);")
#     con.close()


#     # commit to the db 
#     # concept : dbt and this loader are the 2 main process with full access to this db. 
#     # dag loads inmem raw data, dumps into src, then opens the real db, import the data back.
#     # dagster wise, only one process (this dag) shall have the file-based connection. other uses a combo of in mem and import the whole database from src.
#     con = duckdb.connect(dw_path,read_only=False)
#     con.sql("""DROP TABLE IF EXISTS tasks_raw;
#             DROP TABLE IF EXISTS lists_raw;
#             DROP TABLE IF EXISTS folders_raw
#             """)
#     con.sql(f"IMPORT DATABASE '{os.path.dirname(dw_path)}/src';")
#     con.close()

#     # yield the materialization result
#     for name, entity_df in zip(names,entity_df):
#         yield Output(entity_df,output_name=name)
#     # yield Output(names)


# %%
