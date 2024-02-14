from doctest import debug
from enum import unique
from unittest.util import strclass
from pytz import utc
from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
from os import environ
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta,timezone
import logging
from dagster import asset,AssetExecutionContext
from helper.source_env import dotenv_path,secrets_path


cache_path=os.path.join(dotenv_path,'.token-oauth')

load_dotenv(secrets_path)
client_id=environ.get('client_id')
client_secret=environ.get('client_secret')
username=environ.get('username')
password=environ.get('password')
redirect_uri=environ.get('redirect_uri')



current_dir=os.path.dirname(os.path.abspath(__file__))
raw_file_path = os.path.join(current_dir,'raw')
tasks_file_path = os.path.join(raw_file_path,'all_tasks.json')
lists_file_path = os.path.join(raw_file_path,'all_lists.json')
folders_file_path = os.path.join(raw_file_path,'all_folders.json')



# import pdb; pdb.set_trace()

auth_client = OAuth2(client_id=client_id,
                     client_secret=client_secret,
                     redirect_uri=redirect_uri,
                     cache_path=cache_path
                     )

client = TickTickClient(username, password, auth_client)



default_start = datetime(2022, 7, 23,tzinfo=timezone.utc)
date_format = '%Y-%m-%dT%H:%M:%S.%f%z'


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def deduplicate(source) -> list:
    """
    checks each item and remove duplicated
    """
    unique_items={}
    unique_list=[]

    for item in source:
        item_id=item.get("id")

        if item_id not in unique_items:
            unique_list.append(item)
            unique_items[item_id]=True
    return unique_list


def _get_completed_tasks(start=None, end=datetime.now(timezone.utc), full_load=True):
    """_summary_
    returns a json string
    internal func - uses tickpy to grab completed tasks from start > end.
    `start` has a default value 2022/07/23 which is the start of my ticktick interactions
    `end` defaults to the runtime date.

    Returns:
        list: all the completed tasks in the interval.
    """
    
    completed_tasks=[] 
    logging.info('start loading tasks')
    if full_load:
        current_date=default_start
    elif not full_load: 
        current_date=start
    while current_date <= end:
        tasks=client.task.get_completed(current_date)
        if tasks != []:
            for task in tasks:
                completed_tasks.append(task)
            logging.info(f'loaded {len(tasks)} new tasks from {current_date}. next interation...')
            
        current_date += timedelta(days=1)
    # completed_tasks=json.dumps(completed_tasks)
    return completed_tasks

def get_completed_task() -> list:
    """
    returns a list the full completed tasks and utilize existing file as cache if available.
    """
    try:
        with open(tasks_file_path,'r') as f:
            cached=json.load(f)
            cached_completed=[item for item in cached if 'completedTime' in item]
            last_cached_date=[item['completedTime'] for item in cached if 'completedTime' in item]
            last_cached_date=max(last_cached_date)
            last_cached_date=datetime.strptime(last_cached_date,date_format)
            last_cached_date=last_cached_date - timedelta(days=1)
            full_load=False
            metadata=last_cached_date
    except FileNotFoundError:
        logging.info('no cache found. doing full load...')
        cached_completed=[]
        last_cached_date=None
        full_load=True
        metadata=None
    
    # checks existing and append to cached list 
    net_new=_get_completed_tasks(start=last_cached_date,full_load=full_load)

    # concatenate final completed list
    all_completed_tasks=net_new+cached_completed
    all_completed_tasks=deduplicate(all_completed_tasks)
    return all_completed_tasks,metadata
    

def get_new_tasks() -> list:
    new_tasks=client.state['tasks']
    return new_tasks

@asset
def get_all_tasks(context: AssetExecutionContext) -> list:
    new=get_new_tasks()
    context.log.info(f'new tasks : {len(new)}')
    completed,metadata=get_completed_task()
    context.log.info(f'completed tasks : {len(completed)}. cached from : {metadata}')
    all_tasks=new+completed
    return all_tasks

@asset
def get_lists():
    lists = client.state['projects']
    return lists

@asset
def get_folders():
    folders = client.state['project_folders']
    return folders


def _dump_to_file(source:list, target:str):
    """
    takes source then dumps to json raw file 
    """

    with open(target,'w') as f:
        json.dump(source,f,indent=4,)

@asset
def dump_to_file(get_lists,get_folders,get_all_tasks):
    _dump_to_file(get_lists,lists_file_path)
    _dump_to_file(get_folders,folders_file_path)
    _dump_to_file(get_all_tasks,tasks_file_path)
    return None

# lists,folders = get_lists_and_folders()
# tasks=get_all_tasks()




