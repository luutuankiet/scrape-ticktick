# import sys,os; sys.path.append('..')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dagster_dbt import DbtCliResource, dbt_assets,get_asset_key_for_model,get_asset_keys_by_output_name_for_source
from dagster import AssetExecutionContext, asset
from constants import dbt_manifest_path
import shutil


@dbt_assets(manifest=dbt_manifest_path)
def ticktick_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    dbt_invocation = dbt.cli(["run"], context=context)
    yield from dbt_invocation.stream()

    #cleanup the dir after done
    # target_path = dbt_invocation.target_path
    # if target_path.exists():
    #     shutil.rmtree(target_path)

