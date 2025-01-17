import os
from pathlib import Path
from dagster_dbt import DbtCliResource
import helper.source_env

DBT_DIR = Path(__file__).joinpath("..","..","..","dbt_project").resolve(strict=True)
DBT_TARGET_DIR = DBT_DIR.joinpath("target")


dbt = DbtCliResource(project_dir=DBT_DIR,profiles_dir=DBT_DIR)

if not DBT_TARGET_DIR.exists():
    # scaffold the project target dir
    dbt.cli(["deps"], target_path=Path("target")).wait()
    dbt.cli(["compile"], target_path=Path("target")).wait()
    dbt_manifest_path = (
            dbt.cli(
                ["--quiet", "parse"],
                target_path=Path("target"),
            )
            .wait()
            .target_path.joinpath("manifest.json")
        )
else:
    dbt_manifest_path = DBT_DIR.joinpath("target", "manifest.json").resolve(strict=True)