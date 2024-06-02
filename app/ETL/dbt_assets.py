#%%

import sys,os; sys.path.append('..')
from helper.source_env import dw_path,dbt_models_core,dbt_models_metrics,db_url
from dagster_dbt import DbtCliResource, dbt_assets,get_asset_key_for_model,get_asset_keys_by_output_name_for_source
from dagster import AssetExecutionContext, asset
from constants import dbt_manifest_path
from sqlalchemy import create_engine

edges = os.listdir(dbt_models_core) + os.listdir(dbt_models_metrics)
edges = [edge.replace('.sql','') for edge in edges]
edges = [edge for edge in edges if '.yml' not in edge]
# edges = core + metrics
#%%

conn = create_engine(db_url)

@dbt_assets(manifest=dbt_manifest_path)
def ticktick_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@asset(deps={edge for edge in edges})
def dbt_export_duckdb():
    # with conn.connect() as con:
    #     con.sql(f"EXPORT DATABASE '{os.path.dirname(dw_path)}/src' (FORMAT PARQUET);")
    pass
# @asset(deps={edge for edge in edges})
# def dbt_export_duckdb():
#     con = duckdb.connect(dw_path,read_only=True)
#     con.sql(f"EXPORT DATABASE '{os.path.dirname(dw_path)}/src' (FORMAT PARQUET);")
#     con.close()
# %%
