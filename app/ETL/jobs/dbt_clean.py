from dagster import op,job, define_asset_job, in_process_executor, OpExecutionContext
from assets.dbt_assets import ticktick_dbt_assets
from constants import dbt_manifest_path
import shutil


@op
def op_dbt_clean(context: OpExecutionContext):
    target_path = dbt_manifest_path.parent
    context.log.info(f"Cleaning {target_path}...")
    if target_path.exists():
        shutil.rmtree(target_path)


@job(name="dbt_clean",executor_def=in_process_executor)
def job_dbt_clean():
    op_dbt_clean()