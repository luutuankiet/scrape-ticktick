import os
from dagster import asset,AssetExecutionContext
import duckdb
import pandas as pd
from helper.source_env import raw_path


@asset(compute_kind='Python')
def dump_to_motherduck(context: AssetExecutionContext):
    motherduck_token=os.environ.get('motherduck_token')

    entities = ['tasks','lists','folders']

    for entity in entities:
        entity_path = os.path.join(raw_path,f'{entity}.json')
        entity_df = pd.read_json(entity_path,dtype=str)
        try:
            context.log.info(f'loading {entity} to motherduck...')
            con = duckdb.connect(f'md:ticktick_gtd??motherduck_token={motherduck_token}')
            cur = con.cursor()
            cur.sql(f"CREATE OR REPLACE TABLE {entity}_raw as SELECT * FROM entity_df")
            context.log.info(f'loaded {len(entity_df)} rows to {entity}_raw table.')
        finally:
            con.close()
            cur.close()
    return None




