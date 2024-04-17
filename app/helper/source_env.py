import os 
from dotenv import load_dotenv

# from app.ETL.constants import DBT_PROJECT_DIR



# setup paths
current_dir=os.path.dirname(os.path.abspath(__file__))

# source .env from project root to construct dbt paths
project_dotenv_path=os.path.join(current_dir,'..','..','.env')
load_dotenv(project_dotenv_path)

raw_path = os.path.join(current_dir,'..','ETL','raw')
dotenv_path=os.path.join(current_dir,'..','env')
secrets_path = os.path.join(dotenv_path,'.secrets')
service_account_path = os.path.join(dotenv_path,'service_account.json')
ETL_workdir = os.path.join(current_dir,'..','ETL')


dbt_project_dir = os.environ.get('DBT_PROJECT_DIR')
dbt_models_path=os.path.join(dbt_project_dir,'models')
dw_path = os.environ.get("DW_PATH")

dbt_models_core = os.path.join(dbt_models_path,'marts','core')
dbt_models_metrics = os.path.join(dbt_models_path,'marts','metrics')


load_dotenv(secrets_path)