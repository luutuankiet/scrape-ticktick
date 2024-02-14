import duckdb
import os

from source_env import secrets_path
from dotenv import load_dotenv

load_dotenv(secrets_path)

motherduck_token=os.environ.get('motherduck_token')
con = duckdb.connect(f'md:?motherduck_token={motherduck_token}')
con = duckdb.connect('md:ticktick_gtd')
# con.sql("SHOW DATABASES").show()