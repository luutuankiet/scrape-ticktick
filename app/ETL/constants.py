import os
from pathlib import Path
from dagster_dbt import DbtCliResource
from helper.source_env import dbt_project_dir, dbt_target_path


dbt = DbtCliResource(project_dir=dbt_project_dir,profiles_dir=dbt_project_dir)

if not dbt_target_path.exists():
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
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json").resolve(strict=True)