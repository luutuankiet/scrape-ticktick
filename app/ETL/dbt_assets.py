# import sys,os; sys.path.append('..')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
from dagster import AssetExecutionContext, AssetKey
from constants import dbt_manifest_path
import shutil
from helper.source_env import target_schema
from typing import Any, Mapping


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        return super().get_asset_key(dbt_resource_props).with_prefix(target_schema)


@dbt_assets(manifest=dbt_manifest_path, dagster_dbt_translator=CustomDagsterDbtTranslator())
def ticktick_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    dbt_invocation = dbt.cli(["run"], context=context)
    yield from dbt_invocation.stream()

    #cleanup the dir after done
    # target_path = dbt_invocation.target_path
    # if target_path.exists():
    #     shutil.rmtree(target_path)

