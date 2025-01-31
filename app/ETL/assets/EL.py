import os
from dagster import Output, asset,AssetOut, multi_asset, AssetKey
import pandas as pd
import sys; sys.path.append('..') # to allow import helper which is 1 dir away
from helper.source_env import raw_path,ETL_workdir,db_url,target_schema
import time
from sqlalchemy import create_engine,text
from datetime import datetime
import pytz
import humanize
import numpy as np

engine = create_engine(db_url)



@asset(key=AssetKey('init_extract').with_prefix(target_schema))
def init_extract():
    flag = os.path.join(ETL_workdir,'force_sync.flag')
    with open(flag, 'w') as f:
        pass
    timer = 0
    timeout = 60
    while True:
        if os.path.exists(flag):
            time.sleep(1)
            timer+=1
            if timer == timeout:
                raise Exception(f'timeout reached for {timer} ticks.')
        else:
            break

names = ['tasks_raw', 'lists_raw', 'folders_raw']
@multi_asset(
    outs={
        'tasks_raw': AssetOut(key=AssetKey('tasks_raw').with_prefix(target_schema)),
        'lists_raw': AssetOut(key=AssetKey('lists_raw').with_prefix(target_schema)),
        'folders_raw': AssetOut(key=AssetKey('folders_raw').with_prefix(target_schema))

    },
    compute_kind='python',deps=[init_extract]
)
def raw_data():
    with engine.connect() as conn:
        for name in names:
            raw_file_path = os.path.join(raw_path, name + '.json')
            df = pd.read_json(raw_file_path, dtype=str)
            df.columns = df.columns.str.lower()
            if name == 'tasks_raw':
                df['modifiedtime_humanize'] = df['modifiedtime'].apply(humanize_timestamp)
                df['duedate_humanize'] = df['duedate'].apply(humanize_timestamp)
            
            # Use text() to execute the raw SQL command
            conn.execute(text(f"DROP TABLE IF EXISTS {target_schema+'_raw'}.{name}"))
            conn.commit()

            # Insert the data
            df.to_sql(name, engine, index=False, schema=target_schema+'_raw')
       
            yield Output(value=df, output_name=name)
        conn.close()





def humanize_timestamp(ts):
    if pd.isnull(ts) or ts == '' or ts == 'nan':
        return 'default'    
    # Parse the timestamp
    dt = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f%z')
    
    # Convert to desired timezone (Ho Chi Minh)
    target_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    dt = dt.astimezone(target_tz)
    
    # Get current time in the same timezone for comparison
    now = datetime.now(target_tz)
    
    # Humanize the timestamp
    return humanize.naturaltime(now - dt,months=True)