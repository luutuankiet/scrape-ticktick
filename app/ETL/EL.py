#%%
import os
from dagster import AssetMaterialization, Output, asset,AssetExecutionContext,AssetOut, multi_asset, AssetKey
from dagster_dbt import get_asset_keys_by_output_name_for_source
import duckdb
from duckdb import ConnectionException
import pandas as pd
import sys; sys.path.append('..') # to allow import helper which is 1 dir away
from helper.source_env import raw_path,dw_path
import dbt_assets
#%%

@multi_asset(
    outs={
        name: AssetOut(key=asset_key)
        for name, asset_key in get_asset_keys_by_output_name_for_source(
            [dbt_assets.ticktick_dbt_assets], "raw_data"
        ).items()
    },
    compute_kind='python'
)
def dump_to_motherduck(context: AssetExecutionContext):

    names = ['source_todo_analytics_raw_data_tasks_raw', 'source_todo_analytics_raw_data_lists_raw', 'source_todo_analytics_raw_data_folders_raw']

    tasks_path = os.path.join(raw_path,'tasks.json')
    tasks_df = pd.read_json(tasks_path,dtype=str)
    lists_path = os.path.join(raw_path,'lists.json')
    lists_df = pd.read_json(lists_path,dtype=str)
    folders_path = os.path.join(raw_path,'folders.json')
    folders_df = pd.read_json(folders_path,dtype=str)
    entity_df = [tasks_df,lists_df,folders_df]

    duckdb.close()
    con = duckdb.connect(read_only=False)
# con = duckdb.connect(dw_path,read_only=True)
    con.sql("""CREATE OR REPLACE TABLE tasks_raw as SELECT * FROM tasks_df;
            CREATE OR REPLACE TABLE lists_raw as SELECT * FROM lists_df;
            CREATE OR REPLACE TABLE folders_raw as SELECT * FROM folders_df
            """)
    con.sql(f"EXPORT DATABASE '{os.path.dirname(dw_path)}/src' (FORMAT PARQUET);")
    # context.log.info(f'loaded {len(entity_df)} rows to {entity}_raw table.')
    con.close()


    # commit to the db 
    con = duckdb.connect(dw_path,read_only=False)
    con.sql("""DROP TABLE IF EXISTS tasks_raw;
            DROP TABLE IF EXISTS lists_raw;
            DROP TABLE IF EXISTS folders_raw
            """)
    con.sql(f"IMPORT DATABASE '{os.path.dirname(dw_path)}/src';")
    con.close()

    # yield the materialization result
    for name, entity_df in zip(names,entity_df):
        yield Output(entity_df,output_name=name)
    # yield Output(names)


