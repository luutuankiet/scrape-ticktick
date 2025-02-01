from dagster import define_asset_job
from assets.dbt_assets import ticktick_dbt_assets
from assets.EL import raw_data, init_extract

ETL_job = define_asset_job(
    "dbt_run",
    selection=[
        ticktick_dbt_assets, 
        init_extract, 
        raw_data
        ],
    config=
            {
                "ops": {
                    "ticktick_dbt_assets": {
                        "config": {
                            "cli_args": [
                                "run"
                            ]
                        }
                    }
                }
            },
)

ETL_full_job = define_asset_job(
    "dbt_build",
    selection=[
        ticktick_dbt_assets, 
        init_extract, 
        raw_data
        ],
    config=
            {
                "ops": {
                    "ticktick_dbt_assets": {
                        "config": {
                            "cli_args": [
                                "build"
                            ]
                        }
                    }
                }
            }
)
