import os
from pathlib import Path
from dagster_dbt import DbtCliResource

DBT_PROJECT_DIR = os.environ.get("DBT_PROJECT_DIR")
DBT_PROFILES_DIR=os.environ.get("DBT_PROFILES_DIR")

dbt = DbtCliResource(project_dir=DBT_PROFILES_DIR,profiles_dir=DBT_PROFILES_DIR)

dbt_manifest_path = os.path.join(DBT_PROJECT_DIR,"target", "manifest.json")