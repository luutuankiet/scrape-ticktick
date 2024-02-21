# a standalone job to run once and stay on for the duration of the machine.
# this helps retain one tick tick api call in the duration.

from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
from os import environ
import json
import os
from datetime import datetime, timedelta,timezone
import logging
from helper.source_env import dotenv_path,raw_path
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

cache_path=os.path.join(dotenv_path,'.token-oauth')

client_id=environ.get('client_id')
client_secret=environ.get('client_secret')
username=environ.get('username')
password=environ.get('password')
redirect_uri=environ.get('redirect_uri')

tasks_file_path = os.path.join(raw_path,'tasks.json')
lists_file_path = os.path.join(raw_path,'lists.json')
folders_file_path = os.path.join(raw_path,'folders.json')

default_start = datetime(2022, 7, 23,tzinfo=timezone.utc)
date_format = '%Y-%m-%dT%H:%M:%S.%f%z'


# class TickTickClientWrapper:
#     """
#     wrapper so that the ticktick client class wont be triggered by arbitrary server events like dagster webserver checks.
#     goal : create a single client instance that all funcs subscribes to.
#     """
#     _instance = None


#     # this __new__ func is called whenever this wrapper class is called. 
#     def __new__(cls,client_id,client_secret,username,password,redirect_uri,cache_path):
#         if not cls._instance:
#             cls._instance = super(TickTickClientWrapper, cls).__new__(cls)
#             cls._instance.client_id = client_id
#             cls._instance.client_secret = client_secret
#             cls._instance.username = username
#             cls._instance.password = password
#             cls._instance.redirect_uri = redirect_uri
#             cls._instance.cache_path = cache_path
#             cls._instance.client = None
#         return cls._instance 
#     # this makes sure only a single instance of the class is used across the module whichever func calls this class.
#     # the _instance attribute now holds all the suceeding function's output.


#     def _initialize_client(self):
#         auth_client = OAuth2(client_id=self.client_id,
#                     client_secret=self.client_secret,
#                     redirect_uri=self.redirect_uri,
#                     cache_path=self.cache_path
#                     )
#         self.client = TickTickClient(self.username, self.password, auth_client)
    
#     def get_client(self):
#         if self.client is None:
#             self._initialize_client()
#         return self.client

# # one time call the client instance.
# wrapper = TickTickClientWrapper(client_id,client_secret,username,password,redirect_uri,cache_path)


auth_client = OAuth2(client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    cache_path=cache_path
                    )
client = TickTickClient(username, password, auth_client)


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
    # client=wrapper.get_client()

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
    # client = wrapper.get_client()
    new_tasks=client.state['tasks']
    return new_tasks


def extract_json():
    # task
    new=get_new_tasks()
    logging.info(f'new tasks : {len(new)}')
    completed,metadata=get_completed_task()
    logging.info(f'completed tasks : {len(completed)}. cached from : {metadata}')
    all_tasks=new+completed
    logging.info(f'all tasks : {len(all_tasks)}')
    

    # client = wrapper.get_client()

    # list
    lists = client.state['projects']

    # folders
    folders = client.state['project_folders']

    
    return all_tasks,folders,lists



def _dump_to_file(source:list, target:str):
    """
    takes source then dumps to json raw file 
    """

    with open(target,'w') as f:
        json.dump(source,f,indent=4,)

def dump_to_file(extract_json):
    all_tasks,folders,lists = extract_json
    _dump_to_file(lists,lists_file_path)
    _dump_to_file(folders,folders_file_path)
    _dump_to_file(all_tasks,tasks_file_path)
    return None

if __name__ == '__main__':
    while True:
        sleep_time = 20
        logging.info('start loading...')
        # extract_json()
        dump_to_file(extract_json())
        logging.info(f'done loading. next iteration in {sleep_time} seconds...')
        client.task._client.sync()
        time.sleep(sleep_time)
        