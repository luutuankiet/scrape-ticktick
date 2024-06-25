#%%
import os
from dagster import Output, asset,AssetOut, multi_asset, AssetKey
import pandas as pd
import sys; sys.path.append('..') # to allow import helper which is 1 dir away
from helper.source_env import raw_path,dw_path,ETL_workdir,db_url,target_schema
import time
from sqlalchemy import create_engine
#%%

engine = create_engine(db_url)



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

names = ['tasks_raw', 'lists_raw', 'folders_raw']
@multi_asset(
    outs={
        'tasks_raw': AssetOut(key=AssetKey('tasks_raw')),
        'lists_raw': AssetOut(key=AssetKey('lists_raw')),
        'folders_raw': AssetOut(key=AssetKey('folders_raw'))

    },
    compute_kind='python',deps=[init_extract]
)
def raw_data():
    for name in names:
        raw_file_path = os.path.join(raw_path,name+'.json')
        df = pd.read_json(raw_file_path,dtype=str)
        df.columns = df.columns.str.lower()
        df.to_sql(name, engine, if_exists='replace', index=False, schema=target_schema+'_raw')
   
        yield Output(value=df,output_name=name)
