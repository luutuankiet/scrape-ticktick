import os 
from dotenv import load_dotenv
# setup paths
current_dir=os.path.dirname(os.path.abspath(__file__))
raw_path = os.path.join(current_dir,'..','ETL','raw')
dotenv_path=os.path.join(current_dir,'..','env')
secrets_path = os.path.join(dotenv_path,'.secrets')
project_dotenv_path=os.path.join(current_dir,'..','..','.env')
load_dotenv(secrets_path)