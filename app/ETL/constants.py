import os
from pathlib import Path
from dagster_dbt import DbtCliResource

DBT_PROJECT_DIR = os.environ.get("DBT_PROJECT_DIR")
DBT_PROFILES_DIR=os.environ.get("DBT_PROFILES_DIR")

dbt = DbtCliResource(project_dir=DBT_PROFILES_DIR,profiles_dir=DBT_PROFILES_DIR)

if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD") == 1:
    dbt_manifest_path = (
        dbt.cli(
            ["--quiet", "parse"],
            target_path=Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = os.path.join(DBT_PROJECT_DIR,"target", "manifest.json")