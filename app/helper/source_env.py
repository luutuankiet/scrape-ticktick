import os 
# setup paths
current_dir=os.path.dirname(os.path.abspath(__file__))
dotenv_path=os.path.join(current_dir,'..','env')
secrets_path = os.path.join(dotenv_path,'.secrets')
