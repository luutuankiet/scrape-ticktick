import os
from pathlib import Path
from dagster_dbt import DbtCliResource
# from helper.source_env import project_dotenv_path
# from dotenv import load_dotenv


# load_dotenv(project_dotenv_path)

# dbt_project_dir = Path(__file__).joinpath("..", "..","dbt_project").resolve()
DBT_PROJECT_DIR = os.environ.get("DBT_PROJECT_DIR")
DBT_PROFILES_DIR=os.environ.get("DBT_PROFILES_DIR")

dbt = DbtCliResource(project_dir=DBT_PROFILES_DIR,profiles_dir=DBT_PROFILES_DIR)

# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.
# if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
#     dbt_manifest_path = (
#         dbt.cli(
#             ["--quiet", "parse"],
#             target_path=Path("target"),
#         )
#         .wait()
#         .target_path.joinpath("manifest.json")
#     )
# else:
dbt_manifest_path = os.path.join(DBT_PROJECT_DIR,"target", "manifest.json")