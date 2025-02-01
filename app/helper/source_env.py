import os 
from dotenv import load_dotenv
import urllib.parse
from pathlib import Path



def find_project_root(current_dir, marker_file='.env'):
    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, marker_file)):
            return current_dir
        current_dir = Path(os.path.dirname(current_dir)).resolve(strict=True)
    raise RuntimeError("Project root with marker file '{}' not found.".format(marker_file))

# Find the project root
current_dir = Path(__file__).parent.resolve(strict=True)
project_root = find_project_root(current_dir)


# Load .env from project root
project_dotenv_path = project_root.joinpath('.env')
load_dotenv(project_dotenv_path)




makefile_path = project_root.joinpath('Makefile')
makefile_dir = project_root

raw_path = current_dir.joinpath('..', 'ETL', 'raw').resolve()
if not raw_path.exists():
    os.makedirs(raw_path)

ETL_env_path = current_dir.joinpath('..', 'env').resolve(strict=True)
secrets_path = ETL_env_path.joinpath('.secrets')
service_account_path = ETL_env_path.joinpath('service_account.json')
ETL_workdir = current_dir.joinpath('..', 'ETL').resolve(strict=True)


load_dotenv(secrets_path)



dbt_project_dir = project_root.joinpath('ticktick-py-dbt')
dbt_target_path=dbt_project_dir.joinpath('target')
dbt_models_path=dbt_project_dir.joinpath('models')


dbt_models_core = dbt_models_path.joinpath('marts','core').resolve(strict=True)
dbt_models_metrics = dbt_models_path.joinpath('marts','metrics').resolve(strict=True)

# db connection
user=os.environ.get('DW_USER')
password=os.environ.get('DW_PASSWORD')
database=os.environ.get('DW_DBNAME')
hostname=os.environ.get('DW_HOST')
port=os.environ.get('DW_PORT')
password_encoded = urllib.parse.quote(password)
target_schema = os.environ.get('TARGET_SCHEMA','dev')
db_url = f'postgresql://{user}:{password_encoded}@{hostname}:{port}/{database}?options='
db_url = db_url + f'-csearch_path=={target_schema}'
