import os 
from dotenv import load_dotenv
import urllib.parse



def find_project_root(current_dir, marker_file='.env'):
    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, marker_file)):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise RuntimeError("Project root with marker file '{}' not found.".format(marker_file))

# Find the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = find_project_root(current_dir)


# Load .env.bootstrap

dotenv_bootstrap_path = os.path.join(project_root, '.env.bootstrap')
load_dotenv(dotenv_bootstrap_path)



# Load .env from project root
project_dotenv_path = os.path.join(project_root, '.env')
load_dotenv(project_dotenv_path)



makefile_path = os.environ.get('MAKEFILE_PATH')
makefile_dir = os.path.dirname(makefile_path)

raw_path = os.path.join(current_dir,'..','ETL','raw')
ETL_env_path=os.path.join(current_dir,'..','env')
secrets_path = os.path.join(ETL_env_path,'.secrets')
service_account_path = os.path.join(ETL_env_path,'service_account.json')
ETL_workdir = os.path.join(current_dir,'..','ETL')

load_dotenv(secrets_path)



dbt_project_dir = os.environ.get('DBT_PROJECT_DIR')
dbt_models_path=os.path.join(dbt_project_dir,'models')
dw_path = os.environ.get("DW_PATH")
st_logs_path = os.environ.get("ST_LOGS_PATH")
venv_path = os.environ.get("VIRTUAL_ENV")


dbt_models_core = os.path.join(dbt_models_path,'marts','core')
dbt_models_metrics = os.path.join(dbt_models_path,'marts','metrics')

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
