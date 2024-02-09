from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
from os import environ
from dotenv import load_dotenv

# setup 
load_dotenv('../.secrets')
client_id=environ.get('client_id')
client_secret=environ.get('client_secret')
username=environ.get('username')
password=environ.get('password')
redirect_uri=environ.get('redirect_uri')

auth_client = OAuth2(client_id=client_id,
                     client_secret=client_secret,
                     redirect_uri=redirect_uri)

client = TickTickClient(username, password, auth_client)


client.access_token