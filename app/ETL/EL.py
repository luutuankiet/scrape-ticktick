import os
from dagster import AssetMaterialization, asset,AssetExecutionContext,AssetOut, multi_asset, AssetKey
from dagster_dbt import get_asset_keys_by_output_name_for_source
import duckdb
import pandas as pd
from helper.source_env import raw_path
from . import dbt_assets


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
            asset_key = AssetKey(name=f"{entity}_raw")

            # yield the materialization result
            yield AssetMaterialization(asset_key=asset_key,
                                       metadata={'num_rows': len(entity_df)},
                                       description=f'Successfully loaded {len(entity_df)} rows to {entity}_raw table.'
                                       )
        finally:
            con.close()
            cur.close()



