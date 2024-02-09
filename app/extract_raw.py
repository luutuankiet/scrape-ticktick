from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
from os import environ
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta

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


new_tasks=client.state['tasks']
completed_tasks=[]
start = datetime(2022, 7, 23)
file_path = 'raw/all_tasks.json'

def get_completed_tasks(start=start, end=datetime.now(), full_load=True):
    print('start loading tasks')
    if full_load:
        current_date = start
    else: 
        current_date = datetime.now()
        with open(file_path,'r') as f:
            completed_tasks=json.load(f)
    while current_date <= end:
        tasks=client.task.get_completed(current_date)
        if tasks != []:
            for task in tasks:
                completed_tasks.append(task)
            print(f'loaded {len(tasks)} new tasks from {current_date}. next interation...')
        current_date += timedelta(days=1)
    return completed_tasks


def get_lists_and_folders():
    projects = client.state['projects']
    folders = client.state['project_folders']
    return projects, folders

def dump_raw():
    all_tasks=completed_tasks+new_tasks
    # TODO : complete the dump interatino 

    with open(file_path,'w') as f:
        json.dump(all_tasks,f,indent=4)



if __name__ == '__main__':
    get_completed_tasks()
    dump_raw()