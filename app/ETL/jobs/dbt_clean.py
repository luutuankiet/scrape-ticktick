from dagster import op,job, define_asset_job, in_process_executor, OpExecutionContext
from dbt_assets import ticktick_dbt_assets
from constants import dbt_manifest_path
import shutil


# dbt_clean = ticktick_dbt_assets
# dbt_clean.context = None

# job_dbt_clean = define_asset_job(
#     "dbt_clean",selection=[
#                 dbt_clean
#             ],
#     executor_def=in_process_executor,
#     config={"ops": {"ticktick_dbt_assets": {"config": {"cli_args": ["clean"]}}}},
#     )



@op
def dbt_clean(context: OpExecutionContext):
    target_path = dbt_manifest_path.parent
    context.log.info(f"Cleaning {target_path}...")
    if target_path.exists():
        shutil.rmtree(target_path)


@job(executor_def=in_process_executor)
def job_dbt_clean():
    dbt_clean()